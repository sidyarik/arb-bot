import requests
from core.models import MarketData


BYBIT_SPOT_URL = "https://api.bybit.com/v5/market/tickers?category=spot"
BYBIT_FUTURES_URL = "https://api.bybit.com/v5/market/tickers?category=linear"


def detect_bybit_interval(symbol_data):

    # Bybit сейчас в основном 8h, но оставляем гибкость
    interval = symbol_data.get("fundingIntervalHour")

    try:
        return int(interval)
    except:
        return 8


def fetch_bybit():

    spot_resp = requests.get(BYBIT_SPOT_URL, timeout=10).json()
    fut_resp = requests.get(BYBIT_FUTURES_URL, timeout=10).json()

    spot_list = spot_resp.get("result", {}).get("list", [])
    fut_list = fut_resp.get("result", {}).get("list", [])

    fut_map = {x["symbol"]: x for x in fut_list}

    results = []

    for spot in spot_list:

        symbol = spot.get("symbol")

        if not symbol or not symbol.endswith("USDT"):
            continue

        if symbol not in fut_map:
            continue

        fut = fut_map[symbol]

        funding_rate = float(fut.get("fundingRate", 0))
        funding_interval = detect_bybit_interval(fut)

        market = MarketData(
            exchange="bybit",
            symbol=symbol,

            spot_bid=float(spot.get("bid1Price", 0)),
            spot_ask=float(spot.get("ask1Price", 0)),

            futures_bid=float(fut.get("bid1Price", 0)),
            futures_ask=float(fut.get("ask1Price", 0)),

            funding_rate=funding_rate,
            funding_interval_hours=funding_interval,

            borrow_rate=None,
            borrow_available=True,

            deposit_enabled=True,
            withdraw_enabled=True
        )

        results.append(market)

    return results