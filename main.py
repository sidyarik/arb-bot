from core.aggregator import collect_all_markets
from strategies.cross_exchange import filter_opportunities
from notifier.telegram_bot import TelegramNotifier
import config


sent_cache = set()


async def engine_loop(context):

    try:
        markets = collect_all_markets()

        # 🔥 теперь filter принимает markets
        filtered = filter_opportunities(markets)

        for opp in filtered:

            key = (
                opp.symbol,
                opp.spot_exchange,
                opp.futures_exchange
            )

            if key in sent_cache:
                continue

            message = (
                f"🚨 CROSS-EXCHANGE OPPORTUNITY\n\n"
                f"{opp.symbol}\n"
                f"SELL SPOT: {opp.spot_exchange} @ {opp.spot_price}\n"
                f"LONG FUTURES: {opp.futures_exchange} @ {opp.futures_price}\n"
                f"Spread: {opp.spread * 100:.4f}%\n"
                f"Funding: {opp.funding_rate * 100:.4f}%\n"
            )

            await context.bot.send_message(
                chat_id=config.TELEGRAM_CHAT_ID,
                text=message
            )

            sent_cache.add(key)

        # обновляем память
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