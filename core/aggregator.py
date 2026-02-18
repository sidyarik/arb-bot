from scanner.binance import fetch_binance
from scanner.bybit import fetch_bybit
from scanner.okx import fetch_okx
from scanner.gate import fetch_gate


def safe_fetch(fetch_func, name):
    try:
        return fetch_func()
    except Exception as e:
        print(f"{name.upper()} ERROR:", e)
        return []


def collect_all_markets():
    data = []

    data.extend(safe_fetch(fetch_binance, "binance"))
    data.extend(safe_fetch(fetch_bybit, "bybit"))
    data.extend(safe_fetch(fetch_okx, "okx"))
    data.extend(safe_fetch(fetch_gate, "gate"))

    markets = {}

    for item in data:
        if item.symbol not in markets:
            markets[item.symbol] = {}

        markets[item.symbol][item.exchange] = item

    return markets