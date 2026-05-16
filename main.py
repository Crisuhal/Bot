from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import qrcode, requests, feedparser, os

# Saludo
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola buenas!")

# Clima
async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ciudad = "Quilmes"
    api_key = os.getenv("OPENWEATHER_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
    data = requests.get(url).json()
    temp = data["main"]["temp"]
    await update.message.reply_text(f"El clima en {ciudad} es {temp}°C")

# Generar QR
async def generar_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = " ".join(context.args)
    img = qrcode.make(texto)
    img.save("qr.png")
    await update.message.reply_photo(open("qr.png", "rb"))

# Noticias
async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feed = feedparser.parse("https://www.lanacion.com.ar/rss/")
    items = [entry.title for entry in feed.entries[:5]]
    await update.message.reply_text("\n".join(items))

# Radios
async def radio_provincia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎙️ Radio Provincia en vivo: https://provinciaradio.com.ar/am.php")

async def radio_lared(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎙️ Radio La Red en vivo: https://www.lared.am/")

async def radio_mitre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎙️ Radio Mitre en vivo: https://radiomitre.cienradios.com/")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clima", clima))
    app.add_handler(CommandHandler("qr", generar_qr))
    app.add_handler(CommandHandler("noticias", noticias))
    app.add_handler(CommandHandler("provincia", radio_provincia))
    app.add_handler(CommandHandler("lared", radio_lared))
    app.add_handler(CommandHandler("mitre", radio_mitre))

    app.run_polling()

if __name__ == "__main__":
    main()
