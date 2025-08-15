import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Variables ---
TOKEN = os.getenv("BOT_TOKEN")  # Debe coincidir con el nombre en Variables de Entorno en Render
PORT = int(os.environ.get('PORT', 8443))
APP_URL = "https://genbott-1.onrender.com"  # Cambia por tu URL en Render

# --- Servidor Flask ---
app = Flask(__name__)

# --- Comandos del bot ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Estoy vivo en Render usando Webhooks 🚀")

# --- Inicialización del bot ---
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# --- Ruta para recibir actualizaciones de Telegram ---
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.update_queue.put(update)
    return "ok"

# --- Ruta raíz ---
@app.route("/")
def home():
    return "Bot de Telegram activo con Webhooks ✅"

async def main():
    # Inicializar el bot
    await application.initialize()
    await application.bot.set_webhook(url=f"{APP_URL}/{TOKEN}")
    await application.start()

if __name__ == "__main__":
    # Ejecutar bot en segundo plano
    asyncio.get_event_loop().create_task(main())

    # Iniciar servidor Flask
    app.run(host="0.0.0.0", port=PORT)


