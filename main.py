import asyncio

from core.aggregator import collect_all_markets
from core.market_engine import build_opportunities
from strategies.cross_exchange import filter_opportunities
from telegram_bot import TelegramNotifier
import config


async def engine_loop(notifier: TelegramNotifier):

    while True:
        try:
            markets = collect_all_markets()

            opportunities = build_opportunities(markets)

            filtered = filter_opportunities(opportunities)

            for opp in filtered:

                message = (
                    f"🚨 CROSS-EXCHANGE OPPORTUNITY\n\n"
                    f"{opp.symbol}\n\n"
                    f"SELL SPOT: {opp.spot_exchange} @ {opp.spot_price}\n"
                    f"LONG FUTURES: {opp.futures_exchange} @ {opp.futures_price}\n\n"
                    f"Spread: {opp.spread * 100:.4f}%\n"
                    f"Funding: {opp.funding_rate * 100:.4f}%\n"
                )

                await notifier.send_alert(message)

        except Exception as e:
            print("ENGINE ERROR:", e)

        await asyncio.sleep(config.SCAN_INTERVAL_SEC)


async def main():

    notifier = TelegramNotifier()

    # Запускаем engine как фоновую задачу
    asyncio.create_task(engine_loop(notifier))

    # Запускаем telegram polling внутри текущего loop
    await notifier.app.initialize()
    await notifier.app.start()
    await notifier.app.updater.start_polling()

    print("🚀 Cross-exchange arb engine started")

    # Держим процесс живым
    await notifier.app.updater.idle()


if __name__ == "__main__":
    asyncio.run(main())