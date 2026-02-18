from core.aggregator import collect_all_markets
from core.market_engine import build_opportunities
from strategies.cross_exchange import filter_opportunities
from notifier.telegram_bot import TelegramNotifier
import config


async def engine(context):

    try:
        markets = collect_all_markets()

        opportunities = build_opportunities(markets)

        filtered = filter_opportunities(opportunities)

        for opp in filtered:

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

    except Exception as e:
        print("ENGINE ERROR:", e)


def main():

    notifier = TelegramNotifier()

    app = notifier.app

    app.job_queue.run_repeating(
        engine,
        interval=config.SCAN_INTERVAL_SEC,
        first=5
    )

    app.run_polling()


if __name__ == "__main__":
    main()