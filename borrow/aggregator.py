from borrow.binance_margin import fetch_binance_margin


def collect_borrow_sources():

    result = {}

    binance_assets = fetch_binance_margin()

    for symbol in binance_assets:
        result[symbol] = ["Binance Margin"]

    print(f"[BORROW] Total borrowable: {len(result)}")

    return result