import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Configuración ---
TOKEN = os.getenv("BOT_TOKEN")  # Token desde Variables de Entorno en Render
APP_URL = os.getenv("APP_URL")  # Ejemplo: https://tu-app.onrender.com
PORT = int(os.environ.get("PORT", 8443))

# --- Inicializar Flask ---
app = Flask(__name__)

# --- Inicializar Bot ---
application = Application.builder().token(TOKEN).build()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot activo con Webhooks en Render")

application.add_handler(CommandHandler("start", start))

# --- Webhook ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok", 200

# --- Página principal ---
@app.route("/", methods=["GET"])
def home():
    return "Bot funcionando ✅", 200

if __name__ == "__main__":
    # Configurar Webhook al iniciar
    import asyncio
    async def set_webhook():
        await application.bot.set_webhook(url=f"{APP_URL}/{TOKEN}")
    asyncio.run(set_webhook())

    # Ejecutar Flask
    app.run(host="0.0.0.0", port=PORT)
    




