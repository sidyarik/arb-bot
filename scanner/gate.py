import requests
from core.models import MarketData


GATE_SPOT_URL = "https://api.gateio.ws/api/v4/spot/order_book?currency_pair={}&limit=1"
GATE_FUTURES_URL = "https://api.gateio.ws/api/v4/futures/usdt/order_book?contract={}&limit=1"
GATE_FUNDING_URL = "https://api.gateio.ws/api/v4/futures/usdt/contracts"


def fetch_gate():
    results = []

    try:
        # Получаем список фьючерсных контрактов (там есть funding)
        futures_contracts = requests.get(GATE_FUNDING_URL, timeout=10).json()

        for contract in futures_contracts:

            symbol = contract["name"]  # BTC_USDT
            if not symbol.endswith("_USDT"):
                continue

            spot_symbol = symbol

            try:
                # SPOT
                spot_resp = requests.get(
                    GATE_SPOT_URL.format(spot_symbol),
                    timeout=10
                ).json()

                if not spot_resp.get("bids") or not spot_resp.get("asks"):
                    continue

                spot_bid = float(spot_resp["bids"][0][0])
                spot_ask = float(spot_resp["asks"][0][0])

                # FUTURES
                fut_resp = requests.get(
                    GATE_FUTURES_URL.format(symbol),
                    timeout=10
                ).json()

                if not fut_resp.get("bids") or not fut_resp.get("asks"):
                    continue

                futures_bid = float(fut_resp["bids"][0]["p"])
                futures_ask = float(fut_resp["asks"][0]["p"])

                funding_rate = float(contract.get("funding_rate", 0))

                market = MarketData(
                    exchange="gate",
                    symbol=symbol.replace("_", ""),

                    spot_bid=spot_bid,
                    spot_ask=spot_ask,

                    futures_bid=futures_bid,
                    futures_ask=futures_ask,

                    funding_rate=funding_rate,

                    borrow_rate=None,
                    borrow_available=True
                )

                results.append(market)

            except:
                continue

        return results

    except Exception as e:
        print("GATE ERROR:", e)
        return []