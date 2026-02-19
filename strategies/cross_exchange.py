# strategies/cross_exchange.py

from core.market_engine import build_opportunities
import config


def filter_opportunities(markets: dict):

    raw_opportunities = build_opportunities(markets)
    filtered = []

    print(f"[ENGINE] Markets symbols: {len(markets)}")
    print(f"[ENGINE] Raw opportunities: {len(raw_opportunities)}")

    # 🔥 BORROW LOGIC FIX
    # token borrowable only if ANY exchange says True
    borrowable_symbols = set()

    for symbol, exchanges in markets.items():

        # ЖЁСТКАЯ проверка
        has_real_borrow = any(
            data.borrow_available is True
            for data in exchanges.values()
        )

        if has_real_borrow:
            borrowable_symbols.add(symbol)

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