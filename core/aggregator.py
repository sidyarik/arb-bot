from scanner.binance import fetch_binance
from scanner.bybit import fetch_bybit
from scanner.okx import fetch_okx
from scanner.gate import fetch_gate


def collect_all_markets():
    data = []

    data.extend(fetch_binance())
    data.extend(fetch_bybit())
    data.extend(fetch_okx())
    data.extend(fetch_gate())

    markets = {}

    for item in data:
        if item.symbol not in markets:
            markets[item.symbol] = {}

        markets[item.symbol][item.exchange] = item

    return markets