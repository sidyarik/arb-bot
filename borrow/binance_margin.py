import requests
import time
import hmac
import hashlib
import config


BINANCE_MARGIN_URL = "https://api.binance.com/sapi/v1/margin/allAssets"


def sign_query(query_string: str, secret: str) -> str:
    return hmac.new(
        secret.encode(),
        query_string.encode(),
        hashlib.sha256
    ).hexdigest()


def fetch_binance_margin():

    if not config.BINANCE_API_KEY or not config.BINANCE_SECRET:
        print("[BORROW] Binance API keys missing")
        return set()

    try:
        timestamp = int(time.time() * 1000)

        query_string = f"timestamp={timestamp}"
        signature = sign_query(query_string, config.BINANCE_SECRET)

        headers = {
            "X-MBX-APIKEY": config.BINANCE_API_KEY
        }

        url = f"{BINANCE_MARGIN_URL}?{query_string}&signature={signature}"

        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        if not isinstance(data, list):
            print("[BORROW] Binance unexpected response:", data)
            return set()

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