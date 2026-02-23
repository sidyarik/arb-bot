from borrow.binance_static import BINANCE_STATIC_BORROW
from borrow.bybit_margin import fetch_bybit_margin
from borrow.gate_margin import fetch_gate_margin
from borrow.bybit_loans import fetch_bybit_loans


def collect_borrow_sources():

    result = {}

    # Binance static
    for symbol in BINANCE_STATIC_BORROW:
        result.setdefault(symbol, []).append("Binance Static")

    # Bybit margin
    bybit_assets = fetch_bybit_margin()
    for symbol in bybit_assets:
        result.setdefault(symbol, []).append("Bybit Margin")

    # Gate proxy
    gate_assets = fetch_gate_margin()
    for symbol in gate_assets:
        result.setdefault(symbol, []).append("Gate Proxy")

    # 🔥 Bybit Loans (real data)
    loans = fetch_bybit_loans()

    for symbol, info in loans.items():

        text = (
            f"Bybit Loan "
            f"(APR≈{info['rate']}/h, "
            f"avail={info['available']})"
        )

        result.setdefault(symbol, []).append(text)

    print(f"[BORROW] Total borrowable: {len(result)}")

    return result