from core.market_engine import build_opportunities
import config


MIN_SPREAD = 0.005  # 0.5%


def filter_opportunities(markets: dict):

    raw_opportunities = build_opportunities(markets)

    filtered = []

    for op in raw_opportunities:

        # 1️⃣ токен должен быть доступен для займа
        if not op.borrow_available:
            continue

        # 2️⃣ спред минимум 0.5%
        has_spread = op.spread >= MIN_SPREAD_PERCENT

        # 3️⃣ funding строго отрицательный и ниже порога
        has_funding = op.funding_rate <= -config.FUNDING_THRESHOLD

        if has_spread or has_funding:
            filtered.append(op)

    return filtered