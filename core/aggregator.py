from scanner.binance import fetch_binance
from scanner.bybit import fetch_bybit
from scanner.okx import fetch_okx
from scanner.gate import fetch_gate


def collect_all_markets():
    all_data = []

    # собираем данные со всех бирж
    all_data.extend(fetch_binance())
    all_data.extend(fetch_bybit())
    all_data.extend(fetch_okx())
    all_data.extend(fetch_gate())

    markets = {}

    for item in all_data:
        if item.symbol not in markets:
            markets[item.symbol] = {}

        markets[item.symbol][item.exchange] = item

    return markets