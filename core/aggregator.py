from scanner.binance import fetch_binance
from scanner.bybit import fetch_bybit
from scanner.okx import fetch_okx
from scanner.gate import fetch_gate


def collect_all_markets():

    all_data = []

    try:
        all_data += fetch_binance() or []
    except Exception as e:
        print("BINANCE ERROR:", e)

    try:
        all_data += fetch_bybit() or []
    except Exception as e:
        print("BYBIT ERROR:", e)

    try:
        all_data += fetch_okx() or []
    except Exception as e:
        print("OKX ERROR:", e)

    try:
        all_data += fetch_gate() or []
    except Exception as e:
        print("GATE ERROR:", e)

    markets = {}

    for item in all_data:

        # защита от None
        if item is None:
            continue

        # защита от неправильного типа
        if not hasattr(item, "symbol"):
            continue

        if item.symbol not in markets:
            markets[item.symbol] = {}

        markets[item.symbol][item.exchange] = item

    return markets