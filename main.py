from core.aggregator import collect_all_markets
from strategies.cross_exchange import filter_opportunities
from notifier.telegram_bot import TelegramNotifier
from borrow.aggregator import collect_borrow_sources

import config
import time
import asyncio


sent_cache = set()

borrow_cache = {}
last_borrow_update = 0
BORROW_REFRESH_SEC = 600

MAX_ALERTS_PER_CYCLE = 5


async def engine_loop(context):

    global borrow_cache, last_borrow_update

    try:

        now = time.time()
        if now - last_borrow_update > BORROW_REFRESH_SEC:
            print("Updating borrow cache...")
            borrow_cache = collect_borrow_sources()
            last_borrow_update = now

        markets = collect_all_markets()
        raw_ops = filter_opportunities(markets)

        sent_count = 0

        for opp in raw_ops:

            if sent_count >= MAX_ALERTS_PER_CYCLE:
                break

            key = (
                opp.symbol,
                opp.spot_exchange,
                opp.futures_exchange
            )

            if key in sent_cache:
                continue

            borrow_sources = borrow_cache.get(opp.symbol, [])

            spread = opp.spread
            funding = opp.funding_rate

            spread_ok = spread >= config.MIN_SPREAD_PERCENT
            funding_negative = funding <= -config.FUNDING_THRESHOLD

            tier = None

            # показываем только ситуации где funding платят нам
            if spread_ok and funding_negative:

                if any("Bybit Loan" in s for s in borrow_sources):
                    tier = "TIER A — SPREAD + FUNDING + LOAN"
                else:
                    tier = "TIER B — SPREAD + FUNDING"

            if not tier:
                continue

            if borrow_sources:
                borrow_text = "\n".join([f"• {x}" for x in borrow_sources])
            else:
                borrow_text = "⚠️ Not found in borrow sources"

            d_icon = "🟢 D" if getattr(opp, "deposit_enabled", True) else "🔴 D"
            w_icon = "🟢 V" if getattr(opp, "withdraw_enabled", True) else "🔴 V"

            funding_interval = getattr(opp, "funding_interval_hours", 8)

            message = (
                f"🚨 {tier}\n\n"
                f"{opp.symbol}\n"
                f"SELL SPOT: {opp.spot_exchange} @ {opp.spot_price}\n"
                f"LONG FUTURES: {opp.futures_exchange} @ {opp.futures_price}\n"
                f"Spread: {spread * 100:.4f}%\n"
                f"Funding: {funding * 100:.4f}% "
                f"(every {funding_interval}h)\n"
                f"Borrow available:\n{borrow_text}"
            )

            await context.bot.send_message(
                chat_id=config.TELEGRAM_CHAT_ID,
                text=message
            )

            sent_cache.add(key)
            sent_count += 1

            await asyncio.sleep(0.3)

        current_keys = {
            (op.symbol, op.spot_exchange, op.futures_exchange)
            for op in raw_ops
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