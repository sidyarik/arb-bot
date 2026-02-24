import config
from core.market_engine import build_opportunities


PURE_SPREAD_THRESHOLD = 0.03  # 3%


def classify_opportunity(op, borrow_sources):

    spread = op.spread
    funding = op.funding_rate

    spread_ok = spread >= config.MIN_SPREAD_PERCENT
    funding_negative = funding <= -config.FUNDING_THRESHOLD
    pure_spread_big = (
        spread >= PURE_SPREAD_THRESHOLD
        and funding > -config.FUNDING_THRESHOLD
    )

    # TIER S — чистый спред 3%+
    if pure_spread_big:
        return "TIER S — PURE SPREAD 3%+"

    # Spread + negative funding
    if spread_ok and funding_negative:
        if any("Bybit Loan" in s for s in borrow_sources):
            return "TIER A — SPREAD + FUNDING + LOAN"
        return "TIER B — SPREAD + FUNDING"

    return None


def filter_opportunities(markets: dict):

    raw_opportunities = build_opportunities(markets)
    filtered = []

    for op in raw_opportunities:

        # borrow sources уже будут добавляться в main
        op.tier_name = None
        filtered.append(op)

    return filtered