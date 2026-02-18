from telegram.ext import ApplicationBuilder, CommandHandler
import config


class TelegramNotifier:

    def __init__(self):
        self.app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

    async def start(self, update, context):
        await update.message.reply_text("🚀 Cross-exchange arb engine started")

    def run(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.run_polling()