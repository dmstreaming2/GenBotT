import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # Lo pones en variables de entorno en Render
PORT = int(os.environ.get('PORT', 8443))

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Estoy vivo en Render usando Webhooks 🚀")

application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

@app.post(f"/{TOKEN}")
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

@app.get("/")
def home():
    return "Bot activo con Webhooks ✅"

if __name__ == "__main__":
    import asyncio
    async def main():
        await application.bot.set_webhook(url=f"{APP_URL}/{TOKEN}")
    asyncio.run(main())

    app.run(host="0.0.0.0", port=PORT)






