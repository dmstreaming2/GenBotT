import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Variables ---
TOKEN = os.getenv("BOT_TOKEN")  # Debe coincidir con el nombre en Variables de Entorno
PORT = int(os.environ.get('PORT', 8443))

# URL base de tu app en Render
APP_URL = "https://genbott-1.onrender.com"

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
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# --- Ruta raíz para verificar que está corriendo ---
@app.route("/")
def home():
    return "Bot de Telegram activo con Webhooks ✅"

if __name__ == "__main__":
    # Configurar el webhook en Telegram
    application.bot.set_webhook(url=f"{APP_URL}/{TOKEN}")

    # Iniciar servidor Flask
    app.run(host="0.0.0.0", port=PORT)

