import requests


BINANCE_MARGIN_URL = "https://api.binance.com/sapi/v1/margin/allAssets"


def fetch_binance_margin():

    try:
        r = requests.get(BINANCE_MARGIN_URL, timeout=10)
        data = r.json()

        borrowable = set()

        for item in data:

            if not item.get("isBorrowable"):
                continue

            asset = item.get("asset")

            if not asset:
                continue

            symbol = f"{asset}USDT"
            borrowable.add(symbol)

        print(f"[BORROW] Binance margin: {len(borrowable)} assets")

        return borrowable

    except Exception as e:
        print("[BORROW] Binance error:", e)
        return set()