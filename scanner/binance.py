import ccxt
import config
import time


def scan_opportunities():
    futures = ccxt.binanceusdm({"enableRateLimit": True})
    spot = ccxt.binance({
        "apiKey": config.BINANCE_API_KEY,
        "secret": config.BINANCE_SECRET,
        "enableRateLimit": True
    })

    # 1) loanable tokens (Crypto Loans)
    loanable = set()
    try:
        loan_data = spot.sapiGetLoanLoanableData()
        for item in loan_data:
            loanable.add(item["loanCoin"])
    except:
        return []

    results = []

    funding_rates = futures.fetch_funding_rates()
    futures_markets = futures.load_markets()
    spot_markets = spot.load_markets()

    for symbol, fr in funding_rates.items():
        funding = fr.get("fundingRate")
        if funding is None or funding > config.FUNDING_THRESHOLD:
            continue

        fm = futures_markets.get(symbol)
        if not fm or fm.get("quote") != "USDT":
            continue

        base = fm.get("base")
        if base not in loanable:
            continue

        spot_symbol = f"{base}/USDT"
        if spot_symbol not in spot_markets:
            continue

        try:
            sp = spot.fetch_ticker(spot_symbol)["last"]
            fp = futures.fetch_ticker(symbol)["last"]
            if not sp or not fp:
                continue

            spread = (fp - sp) / sp * 100

            # funding interval (обычно 8h, но берём точно)
            next_funding_ts = fr.get("nextFundingTimestamp")
            hours_to_funding = None
            if next_funding_ts:
                hours_to_funding = round((next_funding_ts - int(time.time()*1000)) / 3_600_000, 2)

            results.append({
                "symbol": symbol,
                "funding": funding,
                "spread": spread,
                "hours_to_funding": hours_to_funding
            })

        except:
            continue

    return results