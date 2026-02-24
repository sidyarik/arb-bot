import requests
from core.models import MarketData
from scanner.binance_transfer import fetch_binance_transfer_status


BINANCE_SPOT_URL = "https://api.binance.com/api/v3/ticker/bookTicker"
BINANCE_FUTURES_URL = "https://fapi.binance.com/fapi/v1/ticker/bookTicker"
BINANCE_FUNDING_URL = "https://fapi.binance.com/fapi/v1/premiumIndex"


def fetch_binance():
    spot_data = requests.get(BINANCE_SPOT_URL, timeout=10).json()
    futures_data = requests.get(BINANCE_FUTURES_URL, timeout=10).json()
    funding_data = requests.get(BINANCE_FUNDING_URL, timeout=10).json()

    futures_map = {item["symbol"]: item for item in futures_data}
    funding_map = {item["symbol"]: item for item in funding_data}

    results = []

    transfer_map = fetch_binance_transfer_status()

    for spot in spot_data:

        symbol = spot["symbol"]

        if not symbol.endswith("USDT"):
            continue

        if symbol not in futures_map:
            continue

        fut = futures_map[symbol]
        funding = funding_map.get(symbol, {})

        market = MarketData(
            exchange="binance",
            symbol=symbol,

            spot_bid=float(spot["bidPrice"]),
            spot_ask=float(spot["askPrice"]),

            futures_bid=float(fut["bidPrice"]),
            futures_ask=float(fut["askPrice"]),

            funding_rate=float(funding.get("lastFundingRate", 0)),

            borrow_rate=None,
            borrow_available=False,

            deposit_enabled=transfer.get("deposit", True),
            withdraw_enabled=transfer.get("withdraw", True)
        )

        results.append(market)

    return results