import config


def filter_opportunities(opportunities):

    filtered = []

    for op in opportunities:

        # 1️⃣ токен должен быть доступен для займа
        if not op.borrow_available:
            continue

        # 2️⃣ фильтр по спреду
        has_spread = op.spread > config.MIN_SPREAD_PERCENT

        # 3️⃣ фильтр по funding (только отрицательный)
        has_funding = op.funding_rate < -config.FUNDING_THRESHOLD

        if has_spread or has_funding:
            filtered.append(op)

    return filtered