import requests


BYBIT_INSTRUMENTS_URL = (
    "https://api.bybit.com/v5/market/instruments-info?category=spot"
)


def fetch_bybit_margin():

    try:
        r = requests.get(BYBIT_INSTRUMENTS_URL, timeout=10)
        data = r.json()

        if data.get("retCode") != 0:
            print("[BORROW] Bybit unexpected response:", data)
            return set()

        result = data.get("result", {})
        items = result.get("list", [])

        borrowable = set()

        for item in items:

            symbol = item.get("symbol")

            if not symbol:
                continue

            if not symbol.endswith("USDT"):
                continue

            # 🔥 главное — margin trading enabled
            if not item.get("marginTrading", False):
                continue

            borrowable.add(symbol)

        print(f"[BORROW] Bybit margin pairs: {len(borrowable)} assets")

        return borrowable

    except Exception as e:
        print("[BORROW] Bybit error:", e)
        return set()