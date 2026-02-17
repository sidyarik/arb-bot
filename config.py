import os

print("ALL ENV VARS:", dict(os.environ))

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
print("TOKEN:", TELEGRAM_TOKEN)

chat_id = os.getenv("TELEGRAM_CHAT_ID")
print("CHAT_ID RAW:", chat_id)

if chat_id is None:
    raise ValueError("TELEGRAM_CHAT_ID NOT FOUND")

TELEGRAM_CHAT_ID = int(chat_id)

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET = os.getenv("BINANCE_SECRET")

FUNDING_THRESHOLD = float(os.getenv("FUNDING_THRESHOLD", -0.0005))
SCAN_INTERVAL_SEC = int(os.getenv("SCAN_INTERVAL_SEC", 120))