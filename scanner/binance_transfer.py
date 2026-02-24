import requests
import time
import hmac
import hashlib
import config


BINANCE_NETWORK_URL = "https://api.binance.com/sapi/v1/capital/config/getall"


def sign_query(query_string: str, secret: str) -> str:
    return hmac.new(
        secret.encode(),
        query_string.encode(),
        hashlib.sha256
    ).hexdigest()


def fetch_binance_transfer_status():

    if not config.BINANCE_API_KEY or not config.BINANCE_SECRET:
        print("[TRANSFER] Binance keys missing")
        return {}

    try:

        timestamp = int(time.time() * 1000)
        query = f"timestamp={timestamp}"
        signature = sign_query(query, config.BINANCE_SECRET)

        headers = {
            "X-MBX-APIKEY": config.BINANCE_API_KEY
        }

        url = f"{BINANCE_NETWORK_URL}?{query}&signature={signature}"

        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        if not isinstance(data, list):
            print("[TRANSFER] Binance error:", data)
            return {}

        result = {}

        for coin in data:

            asset = coin.get("coin")
            networks = coin.get("networkList", [])

            deposit = False
            withdraw = False

            for net in networks:
                if net.get("depositEnable"):
                    deposit = True
                if net.get("withdrawEnable"):
                    withdraw = True

            symbol = f"{asset}USDT"

            result[symbol] = {
                "deposit": deposit,
                "withdraw": withdraw
            }

        print(f"[TRANSFER] Binance assets: {len(result)}")

        return result

    except Exception as e:
        print("[TRANSFER] Binance exception:", e)
        return {}