import requests
import time
from core.models import MarketData
from scanner.binance_transfer import fetch_binance_transfer_status


BINANCE_SPOT_URL = "https://api.binance.com/api/v3/ticker/bookTicker"
BINANCE_FUTURES_URL = "https://fapi.binance.com/fapi/v1/ticker/bookTicker"
BINANCE_FUNDING_URL = "https://fapi.binance.com/fapi/v1/premiumIndex"


def detect_funding_interval(funding_item):

    try:
        next_time = int(funding_item.get("nextFundingTime", 0))
        now = int(time.time() * 1000)

        hours = (next_time - now) / 1000 / 60 / 60

        # округляем к ближайшим стандартным интервалам
        if hours <= 1.5:
            return 1
        elif hours <= 3:
            return 2
        elif hours <= 6:
            return 4
        else:
            return 8

    except:
        return 8


def fetch_binance():

    spot_data = requests.get(BINANCE_SPOT_URL, timeout=10).json()
    futures_data = requests.get(BINANCE_FUTURES_URL, timeout=10).json()
    funding_data = requests.get(BINANCE_FUNDING_URL, timeout=10).json()

    transfer_map = fetch_binance_transfer_status()

    futures_map = {item["symbol"]: item for item in futures_data}
    funding_map = {item["symbol"]: item for item in funding_data}

    results = []

    for spot in spot_data:

        symbol = spot["symbol"]

        if not symbol.endswith("USDT"):
            continue

        if symbol not in futures_map:
            continue

        fut = futures_map[symbol]
        funding = funding_map.get(symbol, {})
        transfer = transfer_map.get(symbol, {})

        funding_interval = detect_funding_interval(funding)

        market = MarketData(
            exchange="binance",
            symbol=symbol,

            spot_bid=float(spot["bidPrice"]),
            spot_ask=float(spot["askPrice"]),

            futures_bid=float(fut["bidPrice"]),
            futures_ask=float(fut["askPrice"]),

            funding_rate=float(funding.get("lastFundingRate", 0)),
            funding_interval_hours=funding_interval,

            borrow_rate=None,
            borrow_available=True,

            deposit_enabled=transfer.get("deposit", True),
            withdraw_enabled=transfer.get("withdraw", True)
        )

        results.append(market)

    return results