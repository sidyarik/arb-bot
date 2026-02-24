PURE_SPREAD_THRESHOLD = 0.03  # 3%


def classify_opportunity(op):

    spread_ok = op.spread >= config.MIN_SPREAD_PERCENT
    funding_ok = op.funding_rate <= -config.FUNDING_THRESHOLD
    pure_spread_big = op.spread >= PURE_SPREAD_THRESHOLD and abs(op.funding_rate) < config.FUNDING_THRESHOLD

    # ТИРЫ
    if pure_spread_big:
        return "TIER S — PURE SPREAD 3%+"

    if spread_ok and funding_ok:
        return "TIER A — SPREAD + FUNDING"

    if funding_ok:
        return "TIER B — FUNDING"

    if spread_ok:
        return "TIER C — SPREAD"

    return None


def filter_opportunities(markets: dict):

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

        tier = classify_opportunity(op)

        if not tier:
            continue

        op.tier_name = tier  # добавляем динамически
        filtered.append(op)

    return filtered