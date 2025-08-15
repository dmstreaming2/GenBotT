import random
from datetime import datetime
from io import BytesIO
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes

# ------------------------
# CONFIGURA TU TOKEN AQUÍ
# ------------------------
TOKEN = "7736480325:AAE6XAIWZflC1jj6uzEx9ilz7ymKP9zSE0I"

# Redes y BINs base de ejemplo
BIN_PREFIXES = {
    "visa": ["4"],
    "mastercard": ["51", "52", "53", "54", "55"],
    "amex": ["34", "37"],
    "random": ["4", "51", "34"]  # mezcla
}

# Algoritmo de Luhn para calcular el dígito de control
def luhn_checksum(number: str) -> int:
    digits = [int(d) for d in number]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return (10 - sum(digits) % 10) % 10

# Generar tarjeta completa
def generate_card(bin_pattern: str) -> str:
    card_number = ""
    for ch in bin_pattern:
        if ch == "x":
            card_number += str(random.randint(0, 9))
        else:
            card_number += ch
    # si hay menos de 15 dígitos antes del último, completamos con random
    while len(card_number) < 15:
        card_number += str(random.randint(0, 9))
    # calcular dígito Luhn
    checksum = luhn_checksum(card_number)
    return card_number + str(checksum)

# Comando /generate
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Parámetros: /generate BIN cantidad [mes] [año] [cvv]
        args = context.args
        if len(args) < 2:
            await update.message.reply_text(
                "Uso: /generate <BIN o network> <cantidad> [MM] [YY] [CVV]\n"
                "Ejemplo: /generate 453211xxxxxxxxxx 10"
            )
            return

        bin_input = args[0].lower()
        cantidad = int(args[1])
        mes = args[2] if len(args) > 2 else None
        anio = args[3] if len(args) > 3 else None
        cvv_input = args[4] if len(args) > 4 else None

        # Si el usuario pone 'visa', 'mastercard', etc.
        if bin_input in BIN_PREFIXES:
            prefix = random.choice(BIN_PREFIXES[bin_input])
            bin_pattern = prefix + "x" * (16 - len(prefix))
        else:
            bin_pattern = bin_input

        tarjetas = []
        for _ in range(cantidad):
            card = generate_card(bin_pattern)

            # Fecha
            if not mes:
                mes_gen = str(random.randint(1, 12)).zfill(2)
            else:
                mes_gen = mes
            if not anio:
                anio_gen = str(random.randint(24, 29))
            else:
                anio_gen = anio

            # CVV
            if not cvv_input:
                if card.startswith("34") or card.startswith("37"):  # Amex
                    cvv_gen = str(random.randint(1000, 9999))
                else:
                    cvv_gen = str(random.randint(100, 999))
            else:
                cvv_gen = cvv_input

            tarjetas.append(f"{card}|{mes_gen}|{anio_gen}|{cvv_gen}")

        # Enviar como texto
        respuesta = "\n".join(tarjetas)
        await update.message.reply_text(f"**Tarjetas generadas:**\n```\n{respuesta}\n```", parse_mode="Markdown")

        # Enviar como archivo .txt
        buffer = BytesIO()
        buffer.write(respuesta.encode())
        buffer.seek(0)
        await update.message.reply_document(InputFile(buffer, filename="bins.txt"))

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Arrancar bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("generate", generate))
    print("Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()
