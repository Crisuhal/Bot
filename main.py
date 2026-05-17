from flask import Flask, request, jsonify
import yt_dlp

# Vercel necesita esta variable de nivel superior
app = Flask(__name__)

# Ruta principal para probar que funciona
@app.route("/")
def home():
    return "Tu API está funcionando 🚀"

# Ruta para convertir YouTube → audio
@app.route("/api/audio", methods=["POST"])
def audio():
    data = request.get_json()
    url = data.get("url")
    output = "/tmp/audio.mp3"

    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': output,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])

    # Devuelve un link (ejemplo, después podés servir el archivo)
    return jsonify({"audio_url": "https://tu-app.vercel.app/audio.mp3"})