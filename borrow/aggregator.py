from borrow.binance_static import BINANCE_STATIC_BORROW
from borrow.bybit_margin import fetch_bybit_margin
from borrow.gate_margin import fetch_gate_margin


def collect_borrow_sources():

    result = {}

    # Binance static
    for symbol in BINANCE_STATIC_BORROW:
        result.setdefault(symbol, []).append("Binance Static")

    # Bybit
    bybit_assets = fetch_bybit_margin()
    for symbol in bybit_assets:
        result.setdefault(symbol, []).append("Bybit Margin")

    # Gate
    gate_assets = fetch_gate_margin()
    for symbol in gate_assets:
        result.setdefault(symbol, []).append("Gate Margin")

    print(f"[BORROW] Total borrowable: {len(result)}")

    return result