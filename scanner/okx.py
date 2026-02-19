import requests
from core.models import MarketData


OKX_SPOT_URL = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"
OKX_SWAP_URL = "https://www.okx.com/api/v5/market/tickers?instType=SWAP"
OKX_FUNDING_URL = "https://www.okx.com/api/v5/public/funding-rate?instId={}"


def fetch_okx():
    try:
        spot_resp = requests.get(OKX_SPOT_URL, timeout=10).json()
        swap_resp = requests.get(OKX_SWAP_URL, timeout=10).json()

        spot_data = spot_resp.get("data", [])
        swap_data = swap_resp.get("data", [])

        swap_map = {}
        for item in swap_data:
            inst_id = item["instId"]  # BTC-USDT-SWAP
            if inst_id.endswith("-SWAP"):
                symbol = inst_id.replace("-SWAP", "")
                swap_map[symbol] = item

        results = []

        for spot in spot_data:
            inst_id = spot["instId"]  # BTC-USDT

            if not inst_id.endswith("USDT"):
                continue

            if inst_id not in swap_map:
                continue

            swap = swap_map[inst_id]

            # funding
            funding_resp = requests.get(
                OKX_FUNDING_URL.format(inst_id + "-SWAP"),
                timeout=10
            ).json()

            funding_data = funding_resp.get("data", [])
            funding_rate = float(funding_data[0]["fundingRate"]) if funding_data else 0.0

            market = MarketData(
                exchange="okx",
                symbol=inst_id.replace("-", ""),

                spot_bid=float(spot["bidPx"]),
                spot_ask=float(spot["askPx"]),

                futures_bid=float(swap["bidPx"]),
                futures_ask=float(swap["askPx"]),

                funding_rate=funding_rate,

                borrow_rate=None,
                borrow_available=False
            )

            results.append(market)

        return results

    except Exception as e:
        print("OKX ERROR:", e)
        return []