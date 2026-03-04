from borrow.binance_static import BINANCE_STATIC_BORROW
from borrow.bybit_margin import fetch_bybit_margin
from borrow.gate_margin import fetch_gate_margin
from borrow.bybit_loans import fetch_bybit_loans


def hourly_to_apr(hourly_rate) -> float:
    try:
        r = float(hourly_rate)

        # Если ставка выглядит как hourly (обычно очень маленькая)
        if r < 0.01:
            return r * 24 * 365 * 100

        # Если Bybit уже вернул дневную или странную ставку
        if r < 1:
            return r * 365 * 100

        # Если уже похоже на процент
        return r

    except:
        return 0.0


def format_number(x):
    try:
        return f"{float(x):,.0f}"
    except:
        return str(x)


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

    # Bybit loans (real)
    loans = fetch_bybit_loans()

    for symbol, info in loans.items():

        rate = float(info.get("rate", 0))
        apr = hourly_to_apr(rate)
        available = format_number(info.get("available", 0))

        text = (
            "Bybit Loan\n"
            f"APR: {apr:.2f}%\n"
            f"Available: {available}"
        )

        result.setdefault(symbol, []).append(text)

    print(f"[BORROW] Total borrowable: {len(result)}")

    return result
