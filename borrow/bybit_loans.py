import requests
import time
import hmac
import hashlib
import config


BYBIT_LOANS_URL = "https://api.bybit.com/v5/spot-margin-trade/data"


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

        data = r.json()

        if data.get("retCode") != 0:
            print("[BORROW] Bybit loans error:", data)
            return {}

        loans = {}

        vip_list = data.get("result", {}).get("vipCoinList", [])

        # Берём только первый уровень (VIP0)
        if not vip_list:
            return {}

        coins = vip_list[0].get("list", [])

        for item in coins:

            coin = item.get("currency")
            if not coin:
                continue

            symbol = f"{coin}USDT"

            rate = float(item.get("hourlyBorrowRate", 0))

            print("DEBUG BYBIT LOAN:", symbol, rate)

            available = float(item.get("maxBorrowingAmount", 0))
            borrowable = item.get("borrowable", False)

            loans[symbol] = {
                "rate": rate,
                "available": available,
                "borrowable": borrowable
            }

        print(f"[BORROW] Bybit loans: {len(loans)} assets")

        return loans

    except Exception as e:
        print("[BORROW] Bybit loans exception:", e)
        return {}
