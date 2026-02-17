import os

def get_required_env(name):
    value = os.environ.get(name)
    if value is None:
        print(f"❌ ENV VARIABLE NOT FOUND: {name}")
        print("Current ENV keys:", list(os.environ.keys()))
        raise RuntimeError(f"{name} not set")
    return value

TELEGRAM_TOKEN = get_required_env("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = int(get_required_env("TELEGRAM_CHAT_ID"))

BINANCE_API_KEY = get_required_env("BINANCE_API_KEY")
BINANCE_SECRET = get_required_env("BINANCE_SECRET")

FUNDING_THRESHOLD = float(os.getenv("FUNDING_THRESHOLD", -0.0005))
SCAN_INTERVAL_SEC = int(os.getenv("SCAN_INTERVAL_SEC", 120))