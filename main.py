import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scanner.binance import scan_opportunities
import config


STATE_FILE = "state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚨 Arbitrage watcher started")


async def watcher(context: ContextTypes.DEFAULT_TYPE):
    state = load_state()
    opportunities = scan_opportunities()

    for item in opportunities:
        key = item["symbol"]
        if state.get(key):
            continue

        msg = (
            f"🚨 LOAN OPPORTUNITY\n\n"
            f"{item['symbol']}\n"
            f"Funding: {item['funding'] * 100:.4f}%\n"
            f"Spread: {item['spread']:.2f}%\n"
        )

        if item["hours_to_funding"] is not None:
            msg += f"Next funding in: {item['hours_to_funding']}h\n"

        await context.bot.send_message(
            chat_id=config.TELEGRAM_CHAT_ID,
            text=msg
        )

        state[key] = True

    current = {o["symbol"] for o in opportunities}
    for k in list(state.keys()):
        if k not in current:
            state[k] = False

    save_state(state)


if __name__ == "__main__":
    # DEBUG
    print("===== ENV DEBUG =====")
    print("TOKEN:", config.TELEGRAM_TOKEN)
    print("CHAT_ID:", config.TELEGRAM_CHAT_ID)
    print("=====================")

    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.job_queue.run_repeating(
        watcher,
        interval=config.SCAN_INTERVAL_SEC,
        first=5
    )

    print("Watcher is running...")
    app.run_polling()