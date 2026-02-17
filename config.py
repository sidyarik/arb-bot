import os

print("=== DEBUG START ===")
print("SERVICE NAME:", os.getenv("RAILWAY_SERVICE_NAME"))
print("ENV NAME:", os.getenv("RAILWAY_ENVIRONMENT_NAME"))
print("ALL ENV KEYS:", list(os.environ.keys()))
print("=== DEBUG END ===")

raise RuntimeError("STOP DEBUG")

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

