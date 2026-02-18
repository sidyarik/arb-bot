import config


def filter_opportunities(opportunities: list):

    filtered = []

    for op in opportunities:

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