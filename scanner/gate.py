import requests
from core.models import MarketData

GATE_SPOT_URL = "https://api.gateio.ws/api/v4/spot/tickers"
GATE_FUTURES_URL = "https://api.gateio.ws/api/v4/futures/usdt/tickers"

# test

def fetch_gate():
    results = []

    try:
        spot_resp = requests.get(GATE_SPOT_URL, timeout=10)
        futures_resp = requests.get(GATE_FUTURES_URL, timeout=10)

        if spot_resp.status_code != 200:
            print("GATE spot error:", spot_resp.status_code)
            return []

        if futures_resp.status_code != 200:
            print("GATE futures error:", futures_resp.status_code)
            return []

        spot_data = spot_resp.json()
        futures_data = futures_resp.json()

        if not isinstance(spot_data, list):
            print("GATE spot not list")
            return []

        if not isinstance(futures_data, list):
            print("GATE futures not list")
            return []

        futures_map = {}

        for f in futures_data:
            symbol = f.get("contract")
            if not symbol:
                continue

            # Gate формат: BTC_USDT
            futures_map[symbol] = f

        for s in spot_data:
            symbol = s.get("currency_pair")

            if not symbol or not symbol.endswith("_USDT"):
                continue

            if symbol not in futures_map:
                continue

            fut = futures_map[symbol]

            try:
                market = MarketData(
                    exchange="gate",
                    symbol=symbol.replace("_", ""),  # BTCUSDT формат

                    spot_bid=float(s["highest_bid"]),
                    spot_ask=float(s["lowest_ask"]),

                    futures_bid=float(fut["highest_bid"]),
                    futures_ask=float(fut["lowest_ask"]),

                    funding_rate=float(fut.get("funding_rate", 0)),

                    borrow_rate=None,
                    borrow_available=True,
                )

                results.append(market)

            except Exception as parse_error:
                print("GATE parse error:", parse_error)
                continue

    except Exception as e:
        print("GATE FETCH ERROR:", e)
        return []

    return results