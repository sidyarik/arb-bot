import requests
import time
import hmac
import hashlib
import config


BYBIT_LOANS_URL = "https://api.bybit.com/v5/spot-margin-trade/loan-info"


def sign(payload: str, secret: str) -> str:
    return hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()


def fetch_bybit_loans():

    if not config.BYBIT_API_KEY or not config.BYBIT_SECRET:
        print("[BORROW] Bybit loans: API keys missing")
        return {}

    try:

        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        query_string = ""

        payload = (
            timestamp
            + config.BYBIT_API_KEY
            + recv_window
            + query_string
        )

        signature = sign(payload, config.BYBIT_SECRET)

        headers = {
            "X-BAPI-API-KEY": config.BYBIT_API_KEY,
            "X-BAPI-SIGN": signature,
            "X-BAPI-SIGN-TYPE": "2",
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": recv_window,
        }

        r = requests.get(
            BYBIT_LOANS_URL,
            headers=headers,
            timeout=10
        )

        # DEBUG — покажет реальный ответ
        print("[BORROW] Bybit loans status:", r.status_code)
        print("[BORROW] Bybit loans raw:", r.text[:300])

        data = r.json()

        if data.get("retCode") != 0:
            print("[BORROW] Bybit loans error:", data)
            return {}

        items = data.get("result", {}).get("list", [])

        loans = {}

        for item in items:

            coin = item.get("coin")
            if not coin:
                continue

            symbol = f"{coin}USDT"

            loans[symbol] = {
                "rate": item.get("hourlyBorrowRate", "0"),
                "available": item.get("maxBorrowingAmount", "0")
            }

        print(f"[BORROW] Bybit loans: {len(loans)} assets")

        return loans

    except Exception as e:
        print("[BORROW] Bybit loans exception:", e)
        return {}