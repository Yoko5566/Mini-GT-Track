import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from deepseek import DeepSeekAPI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

api = DeepSeekAPI(api_key=DEEPSEEK_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    try:
        reply = api.chat_completion(prompt=user_text)
    except Exception as e:
        reply = f"Error: {e}"
    await update.message.reply_text(reply)

def main() -> None:
    if not TELEGRAM_TOKEN or not DEEPSEEK_API_KEY:
        raise EnvironmentError("TELEGRAM_TOKEN and DEEPSEEK_API_KEY must be set")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
