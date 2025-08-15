import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Variables ---
TOKEN = os.getenv("BOT_TOKEN")  # Configurado en Variables de Entorno de Render
PORT = int(os.environ.get('PORT', 8443))
APP_URL = "https://genbott-1.onrender.com"

# --- Servidor Flask ---
app = Flask(__name__)

# --- Inicialización del bot ---
application = Application.builder().token(TOKEN).build()

# --- Comandos ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Bot activo en Render con Webhooks 🚀")

application.add_handler(CommandHandler("start", start))

# --- Ruta para recibir actualizaciones ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# --- Ruta raíz ---
@app.route("/")
def home():
    return "Bot de Telegram activo con Webhooks ✅"

if __name__ == "__main__":
    import asyncio

    async def main():
        # Configurar el webhook
        await application.bot.set_webhook(url=f"{APP_URL}/{TOKEN}")
        # Iniciar servidor Flask
        app.run(host="0.0.0.0", port=PORT)

    asyncio.run(main())



