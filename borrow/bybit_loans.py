import requests


BYBIT_LOANS_URL = "https://api.bybit.com/v5/spot-margin-trade/loan-info"


def fetch_bybit_loans():

    try:
        r = requests.get(BYBIT_LOANS_URL, timeout=10)
        data = r.json()

        if data.get("retCode") != 0:
            print("[BORROW] Bybit loans unexpected:", data)
            return {}

        result = data.get("result", {})
        items = result.get("list", [])

        loans = {}

        for item in items:

            coin = item.get("coin")

            if not coin:
                continue

            symbol = f"{coin}USDT"

            # APR
            borrow_rate = item.get("hourlyBorrowRate", "0")
            available = item.get("maxBorrowingAmount", "0")

            loans[symbol] = {
                "rate": borrow_rate,
                "available": available
            }

        print(f"[BORROW] Bybit loans: {len(loans)} assets")

        return loans

    except Exception as e:
        print("[BORROW] Bybit loans error:", e)
        return {}