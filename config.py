import os

# fallback values (если env не работают)
HARDCODED_BINANCE_KEY = ""
HARDCODED_BINANCE_SECRET = ""

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN") or ""
TELEGRAM_CHAT_ID = int(os.environ.get("TELEGRAM_CHAT_ID", "0"))

BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY") or HARDCODED_BINANCE_KEY
BINANCE_SECRET = os.environ.get("BINANCE_SECRET") or HARDCODED_BINANCE_SECRET

BYBIT_API_KEY = os.environ.get("BYBIT_API_KEY")
BYBIT_SECRET = os.environ.get("BYBIT_SECRET")

OKX_API_KEY = os.environ.get("OKX_API_KEY")
OKX_SECRET = os.environ.get("OKX_SECRET")

GATE_API_KEY = os.environ.get("GATE_API_KEY")
GATE_SECRET = os.environ.get("GATE_SECRET")

MIN_SPREAD_PERCENT = float(
    os.environ.get("MIN_SPREAD_PERCENT", "0.005")
)

FUNDING_THRESHOLD = float(
    os.environ.get("FUNDING_THRESHOLD", "0.0005")
)

SCAN_INTERVAL_SEC = int(
    os.environ.get("SCAN_INTERVAL_SEC", "60"))