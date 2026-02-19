import requests
from core.models import MarketData


BYBIT_SPOT_URL = "https://api.bybit.com/v5/market/tickers?category=spot"
BYBIT_FUTURES_URL = "https://api.bybit.com/v5/market/tickers?category=linear"
BYBIT_FUNDING_URL = "https://api.bybit.com/v5/market/funding/history?category=linear&limit=1"


def fetch_bybit():
    results = []

    try:
        spot_resp = requests.get(BYBIT_SPOT_URL, timeout=10).json()
        futures_resp = requests.get(BYBIT_FUTURES_URL, timeout=10).json()

        if spot_resp.get("retCode") != 0:
            return []

        if futures_resp.get("retCode") != 0:
            return []

        spot_list = spot_resp["result"]["list"]
        futures_list = futures_resp["result"]["list"]

        futures_map = {item["symbol"]: item for item in futures_list}

        for spot in spot_list:

            symbol = spot["symbol"]

            if not symbol.endswith("USDT"):
                continue

            if symbol not in futures_map:
                continue

            fut = futures_map[symbol]

            try:
                market = MarketData(
                    exchange="bybit",
                    symbol=symbol,

                    spot_bid=float(spot["bid1Price"]),
                    spot_ask=float(spot["ask1Price"]),

                    futures_bid=float(fut["bid1Price"]),
                    futures_ask=float(fut["ask1Price"]),

                    funding_rate=float(fut.get("fundingRate", 0)),

                    borrow_rate=None,
                    borrow_available=False
                )

                results.append(market)

            except:
                continue

        return results

    except Exception as e:
        print("BYBIT ERROR:", e)
        return []