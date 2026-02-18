from core.market_engine import build_opportunities
import config


def filter_opportunities(markets: dict):

    # markets: { symbol: { exchange: MarketData } }

    raw_opportunities = build_opportunities(markets)
    filtered = []

    # 🔹 Определяем какие токены вообще можно взять в займ
    borrowable_symbols = set()

    for symbol, exchanges in markets.items():
        for data in exchanges.values():
            if data.borrow_available:
                borrowable_symbols.add(symbol)
                break

    for op in raw_opportunities:

        # 1️⃣ Если токен нигде нельзя взять в займ — пропускаем
        if op.symbol not in borrowable_symbols:
            continue

        # 2️⃣ Проверка спреда
        has_spread = op.spread >= config.MIN_SPREAD_PERCENT

        # 3️⃣ Проверка отрицательного funding
        has_negative_funding = op.funding_rate <= -config.FUNDING_THRESHOLD

        # 4️⃣ Финальная логика
        if has_spread or has_negative_funding:
            filtered.append(op)

    return filtered