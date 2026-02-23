import requests


GATE_SPOT_CURRENCY_PAIRS_URL = "https://api.gateio.ws/api/v4/spot/currency_pairs"


def fetch_gate_margin():

    try:
        r = requests.get(GATE_SPOT_CURRENCY_PAIRS_URL, timeout=10)
        data = r.json()

        if not isinstance(data, list):
            print("[BORROW] Gate unexpected response:", data)
            return set()

        borrowable = set()

        for item in data:

            symbol = item.get("id")

            if not symbol:
                continue

            if not symbol.endswith("_USDT"):
                continue

            if item.get("trade_status") != "tradable":
                continue

            normalized = symbol.replace("_", "")
            borrowable.add(normalized)

        print(f"[BORROW] Gate proxy pairs: {len(borrowable)} assets")

        return borrowable

    except Exception as e:
        print("[BORROW] Gate error:", e)
        return set()