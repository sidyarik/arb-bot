from core.market_engine import build_opportunities
import config


def filter_opportunities(markets: dict):
    raw_opportunities = build_opportunities(markets)

    filtered = []

    for op in raw_opportunities:

        # 1️⃣ Токен должен быть доступен для займа
        if not op.borrow_available:
            continue

        # 2️⃣ Есть спред
        has_spread = op.spread > 0

        # 3️⃣ Есть отрицательный funding (нам платят за лонг)
        has_funding = op.funding_rate < -config.FUNDING_THRESHOLD

        if has_spread or has_funding:
            filtered.append(op)

    return filtered