# strategies/cross_exchange.py

from core.market_engine import build_opportunities
from borrow.aggregator import collect_borrow_sources
import config


def filter_opportunities(markets: dict):

    raw_opportunities = build_opportunities(markets)
    filtered = []

    print(f"[ENGINE] Markets symbols: {len(markets)}")
    print(f"[ENGINE] Raw opportunities: {len(raw_opportunities)}")

    # 🔥 берём borrow из cache-логики
    borrow_cache = collect_borrow_sources()
    borrowable_symbols = set(borrow_cache.keys())

    print(f"[ENGINE] Borrowable symbols: {len(borrowable_symbols)}")

    for op in raw_opportunities:

        if op.symbol not in borrowable_symbols:
            continue

        has_spread = op.spread >= config.MIN_SPREAD_PERCENT

        has_negative_funding = (
            op.funding_rate <= -config.FUNDING_THRESHOLD
        )

        if has_spread or has_negative_funding:
            filtered.append(op)

    print(f"[ENGINE] Filtered opportunities: {len(filtered)}")

    return filtered