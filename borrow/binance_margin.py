import requests


BINANCE_MARGIN_PAIRS_URL = "https://api.binance.com/sapi/v1/margin/allPairs"


def fetch_binance_margin():

    try:
        r = requests.get(BINANCE_MARGIN_PAIRS_URL, timeout=10)
        data = r.json()

        if not isinstance(data, list):
            print("[BORROW] Binance unexpected response:", data)
            return set()

        borrowable = set()

        for item in data:

            # margin trading enabled
            if not item.get("isMarginTrade"):
                continue

            symbol = item.get("symbol")

            if not symbol:
                continue

            # только USDT пары
            if not symbol.endswith("USDT"):
                continue

            borrowable.add(symbol)

        print(f"[BORROW] Binance margin pairs: {len(borrowable)} assets")

        return borrowable

    except Exception as e:
        print("[BORROW] Binance margin pairs error:", e)
        return set()