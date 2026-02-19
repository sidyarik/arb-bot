# borrow/aggregator.py

# ВРЕМЕННАЯ ЗАГЛУШКА (потом заменим на реальные API)

def collect_borrow_sources():

    # symbol -> список мест где можно взять токен
    return {
        "BTCUSDT": ["Binance Margin"],
        "ETHUSDT": ["Binance Margin", "Bybit Loans"],
        "BNBUSDT": ["Binance Margin"],
    }