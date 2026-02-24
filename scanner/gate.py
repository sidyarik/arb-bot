import requests
from core.models import MarketData


GATE_SPOT_URL = "https://api.gateio.ws/api/v4/spot/tickers"
GATE_FUTURES_URL = "https://api.gateio.ws/api/v4/futures/usdt/tickers"


def fetch_gate():

    spot_data = requests.get(GATE_SPOT_URL, timeout=10).json()
    fut_data = requests.get(GATE_FUTURES_URL, timeout=10).json()

    fut_map = {}

    for f in fut_data:
        contract = f.get("contract")
        if contract:
            fut_map[contract.replace("_", "")] = f

    results = []

    for spot in spot_data:

        symbol = spot.get("currency_pair")

        if not symbol or not symbol.endswith("_USDT"):
            continue

        normalized = symbol.replace("_", "")

        if normalized not in fut_map:
            continue

        fut = fut_map[normalized]

        # Gate funding interval почти всегда 8h
        funding_interval = 8

        market = MarketData(
            exchange="gate",
            symbol=normalized,

            spot_bid=float(spot.get("highest_bid", 0)),
            spot_ask=float(spot.get("lowest_ask", 0)),

            futures_bid=float(fut.get("highest_bid", 0)),
            futures_ask=float(fut.get("lowest_ask", 0)),

            funding_rate=float(fut.get("funding_rate", 0)),
            funding_interval_hours=funding_interval,

            borrow_rate=None,
            borrow_available=True,

            deposit_enabled=True,
            withdraw_enabled=True
        )

        results.append(market)

    return results