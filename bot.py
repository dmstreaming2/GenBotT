import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === CONFIGURACIÓN ===
TOKEN = os.getenv("BOT_TOKEN")
APP_URL = "https://genbott-1.onrender.com"
PORT = int(os.environ.get("PORT", 8443))

if not TOKEN:
    raise ValueError("Falta la variable BOT_TOKEN en Render")

# === BOT ===
app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Estoy activo en Render 🚀")

application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "OK"

@app.route("/")
def home():
    return "Bot activo con Webhooks ✅"

if __name__ == "__main__":
    import asyncio
    async def run():
        await application.bot.set_webhook(url=f"{APP_URL}/{TOKEN}")
        app.run(host="0.0.0.0", port=PORT)

    asyncio.run(run())





