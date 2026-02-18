import os

# ==============================
# TELEGRAM
# ==============================

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = int(os.environ.get("TELEGRAM_CHAT_ID", "0"))


# ==============================
# API KEYS (по мере добавления)
# ==============================

BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
BINANCE_SECRET = os.environ.get("BINANCE_SECRET")

BYBIT_API_KEY = os.environ.get("BYBIT_API_KEY")
BYBIT_SECRET = os.environ.get("BYBIT_SECRET")

OKX_API_KEY = os.environ.get("OKX_API_KEY")
OKX_SECRET = os.environ.get("OKX_SECRET")

GATE_API_KEY = os.environ.get("GATE_API_KEY")
GATE_SECRET = os.environ.get("GATE_SECRET")


# ==============================
# STRATEGY SETTINGS
# ==============================

# Минимальный спред между биржами (в процентах)
MIN_SPREAD_PERCENT = float(os.environ.get("MIN_SPREAD_PERCENT", "0.3"))

# Минимальный отрицательный funding (в процентах)
# Например 0.05 = 0.05%
FUNDING_THRESHOLD = float(os.environ.get("FUNDING_THRESHOLD", "0.05"))

# Интервал сканирования
SCAN_INTERVAL_SEC = int(os.environ.get("SCAN_INTERVAL_SEC", "60"))