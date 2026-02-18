import asyncio
from core.aggregator import collect_all_markets
from core.market_engine import build_opportunities
from strategies.cross_exchange import filter_opportunities
from notifier.telegram_bot import TelegramNotifier
import config


sent_cache = set()


async def engine_loop(notifier: TelegramNotifier):

    while True:
        try:
            markets = collect_all_markets()

            opportunities = build_opportunities(markets)

            filtered = filter_opportunities(opportunities)

            for opp in filtered:

                key = (
                    opp.symbol,
                    opp.spot_exchange,
                    opp.futures_exchange
                )

                # 🔒 анти-спам
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

                await notifier.send_alert(message)

                sent_cache.add(key)

            # очищаем кэш если ситуация пропала
            current_keys = {
                (op.symbol, op.spot_exchange, op.futures_exchange)
                for op in filtered
            }

            sent_cache.intersection_update(current_keys)

        except Exception as e:
            print("ENGINE ERROR:", e)

        await asyncio.sleep(config.SCAN_INTERVAL_SEC)


async def main():

    notifier = TelegramNotifier()

    asyncio.create_task(engine_loop(notifier))

    notifier.run()


if __name__ == "__main__":
    asyncio.run(main())