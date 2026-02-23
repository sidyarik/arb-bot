from borrow.binance_static import BINANCE_STATIC_BORROW


def collect_borrow_sources():

    result = {}

    # 🔥 Binance static list
    for symbol in BINANCE_STATIC_BORROW:
        result.setdefault(symbol, []).append("Binance Static")

    print(f"[BORROW] Total borrowable: {len(result)}")

    return result