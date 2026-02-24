import config
from core.market_engine import build_opportunities


PURE_SPREAD_THRESHOLD = 0.03  # 3%


def has_bybit_loan(op):
    # проверяем borrow текст если есть loan
    return any("Bybit Loan" in str(x) for x in getattr(op, "borrow_sources", []))


def classify_opportunity(op, borrow_sources):

    spread = op.spread
    funding = op.funding_rate

    spread_ok = spread >= config.MIN_SPREAD_PERCENT
    funding_negative = funding <= -config.FUNDING_THRESHOLD
    pure_spread_big = (
        spread >= PURE_SPREAD_THRESHOLD
        and funding > -config.FUNDING_THRESHOLD
    )

    # TIER S — только большой чистый спред
    if pure_spread_big:
        return "TIER S — PURE SPREAD 3%+"

    # TIER A — spread + negative funding + bybit loan
    if spread_ok and funding_negative:
        if any("Bybit Loan" in s for s in borrow_sources):
            return "TIER A — SPREAD + FUNDING + LOAN"
        return "TIER B — SPREAD + FUNDING"

    return None


def filter_opportunities(markets: dict, borrow_cache: dict):

    raw_opportunities = build_opportunities(markets)
    filtered = []

    borrowable_symbols = set()

    for symbol, exchanges in markets.items():
        for data in exchanges.values():
            if data.borrow_available:
                borrowable_symbols.add(symbol)
                break

    for op in raw_opportunities:

        if op.symbol not in borrowable_symbols:
            continue

        borrow_sources = borrow_cache.get(op.symbol, [])

        tier = classify_opportunity(op, borrow_sources)

        if not tier:
            continue

        op.tier_name = tier
        op.borrow_sources = borrow_sources

        filtered.append(op)

    return filtered