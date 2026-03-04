import requests


GATE_MARGIN_PAIRS_URL = "https://api.gateio.ws/api/v4/margin/currency_pairs"


def fetch_gate_margin():

    try:
        r = requests.get(GATE_MARGIN_PAIRS_URL, timeout=10)
        data = r.json()

        if not isinstance(data, list):
            print("[BORROW] Gate unexpected response:", data)
            return set()

        borrowable = set()

        for item in data:

            base = item.get("base")
            quote = item.get("quote")

            if not base or not quote:
                continue

            if quote != "USDT":
                continue

            symbol = f"{base}USDT"
            borrowable.add(symbol)

        print(f"[BORROW] Gate margin pairs: {len(borrowable)} assets")

        return borrowable

    except Exception as e:
        print("[BORROW] Gate error:", e)
        return set()