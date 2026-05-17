from telegram.ext import Updater, CommandHandler
import qrcode, requests, feedparser, os
from fpdf import FPDF
import yt_dlp

# Saludo
def start(update, context):
    update.message.reply_text("Hola buenas!")

# Clima
def clima(update, context):
    ciudad = "Quilmes"
    api_key = os.getenv("OPENWEATHER_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
    data = requests.get(url).json()
    temp = data["main"]["temp"]
    update.message.reply_text(f"El clima en {ciudad} es {temp}°C")

# Generar QR
def generar_qr(update, context):
    texto = " ".join(context.args)
    img = qrcode.make(texto)
    img.save("qr.png")
    update.message.reply_photo(open("qr.png", "rb"))

# YouTube a audio
def youtube_audio(update, context):
    url = " ".join(context.args)
    ydl_opts = {'format': 'bestaudio', 'outtmpl': 'audio.mp3'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    update.message.reply_audio(open("audio.mp3", "rb"))

# Noticias
def noticias(update, context):
    feed = feedparser.parse("https://www.lanacion.com.ar/rss/")
    items = [entry.title for entry in feed.entries[:5]]
    update.message.reply_text("\n".join(items))

# Radios
def radio_provincia(update, context):
    update.message.reply_text("🎙️ Radio Provincia en vivo: https://provinciaradio.com.ar/am.php")

def radio_lared(update, context):
    update.message.reply_text("🎙️ Radio La Red en vivo: https://www.lared.am/")

def radio_mitre(update, context):
    update.message.reply_text("🎙️ Radio Mitre en vivo: https://radiomitre.cienradios.com/")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("clima", clima))
    dp.add_handler(CommandHandler("qr", generar_qr))
    dp.add_handler(CommandHandler("yt", youtube_audio))
    dp.add_handler(CommandHandler("noticias", noticias))
    dp.add_handler(CommandHandler("provincia", radio_provincia))
    dp.add_handler(CommandHandler("lared", radio_lared))
    dp.add_handler(CommandHandler("mitre", radio_mitre))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()