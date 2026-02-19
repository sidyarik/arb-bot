# strategies/cross_exchange.py

from core.market_engine import build_opportunities
import config


def filter_opportunities(markets: dict):

    # markets: { symbol: { exchange: MarketData } }

    raw_opportunities = build_opportunities(markets)
    filtered = []

    print(f"[ENGINE] Markets symbols: {len(markets)}")
    print(f"[ENGINE] Raw opportunities: {len(raw_opportunities)}")

    # 🔹 определяем borrowable symbols
    borrowable_symbols = set()

    for symbol, exchanges in markets.items():
        for data in exchanges.values():
            if data.borrow_available:
                borrowable_symbols.add(symbol)
                break

    print(f"[ENGINE] Borrowable symbols: {len(borrowable_symbols)}")

    for op in raw_opportunities:

        # 1️⃣ token должен быть borrowable
        if op.symbol not in borrowable_symbols:
            continue

        # 2️⃣ spread check
        has_spread = op.spread >= config.MIN_SPREAD_PERCENT

        # 3️⃣ funding check
        has_negative_funding = (
            op.funding_rate <= -config.FUNDING_THRESHOLD
        )

        # 4️⃣ final logic
        if has_spread or has_negative_funding:
            filtered.append(op)

    print(f"[ENGINE] Filtered opportunities: {len(filtered)}")

    return filtered