from core.aggregator import collect_all_markets
from core.market_engine import build_opportunities
from strategies.cross_exchange import filter_opportunities
from notifier.telegram_bot import TelegramNotifier
from borrow.aggregator import collect_borrow_sources

import config
import time


sent_cache = set()

# borrow cache
borrow_cache = {}
last_borrow_update = 0
BORROW_REFRESH_SEC = 600  # 10 минут


async def engine_loop(context):

    global borrow_cache, last_borrow_update

    try:

        # 🔥 обновляем borrow редко
        now = time.time()
        if now - last_borrow_update > BORROW_REFRESH_SEC:
            print("Updating borrow cache...")
            borrow_cache = collect_borrow_sources()
            last_borrow_update = now

        markets = collect_all_markets()

        opportunities = build_opportunities(markets)

        filtered = filter_opportunities(opportunities)

        for opp in filtered:

            key = (
                opp.symbol,
                opp.spot_exchange,
                opp.futures_exchange
            )

            if key in sent_cache:
                continue

            borrow_sources = borrow_cache.get(opp.symbol, [])

            # если borrow нет — пропускаем
            if not borrow_sources:
                continue

            borrow_text = "\n".join(
                [f"• {x}" for x in borrow_sources]
            )

            message = (
                f"🚨 CROSS-EXCHANGE OPPORTUNITY\n\n"
                f"{opp.symbol}\n"
                f"SELL SPOT: {opp.spot_exchange} @ {opp.spot_price}\n"
                f"LONG FUTURES: {opp.futures_exchange} @ {opp.futures_price}\n"
                f"Spread: {opp.spread * 100:.4f}%\n"
                f"Funding: {opp.funding_rate * 100:.4f}%\n\n"
                f"Borrow available:\n{borrow_text}"
            )

            await context.bot.send_message(
                chat_id=config.TELEGRAM_CHAT_ID,
                text=message
            )

            sent_cache.add(key)

        current_keys = {
            (op.symbol, op.spot_exchange, op.futures_exchange)
            for op in filtered
        }

        sent_cache.intersection_update(current_keys)

    except Exception as e:
        print("ENGINE ERROR:", e)


def main():

    notifier = TelegramNotifier()

    app = notifier.app

    app.job_queue.run_repeating(
        engine_loop,
        interval=config.SCAN_INTERVAL_SEC,
        first=5
    )

    print("🚀 Cross-exchange arb engine started")

    app.run_polling()


if __name__ == "__main__":
    main()