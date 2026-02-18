from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import config


class TelegramNotifier:
    def __init__(self):
        self.app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🚀 Cross-exchange arb engine started")

    async def send_alert(self, message: str):
        await self.app.bot.send_message(
            chat_id=config.TELEGRAM_CHAT_ID,
            text=message
        )

    def run(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.run_polling()