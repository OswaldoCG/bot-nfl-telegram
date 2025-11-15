import os
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters

# Configuración
TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PORT = int(os.environ.get("PORT", 8080))  # Railway asigna un puerto

if not TOKEN or not GROQ_API_KEY:
    print("Faltan TOKEN o GROQ_API_KEY")
    exit()

bot = Bot(TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)  # Workers=0 para evitar hilos en webhook

# Función que llama a Groq
def generar_respuesta(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"  # Asegúrate de usar tu endpoint
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Eres un asistente conversacional amable y útil."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            print("Error API Groq:", response.status_code, response.text)
            return "Hubo un error con la IA."
        resp_json = response.json()
        if "choices" in resp_json:
            return resp_json["choices"][0]["message"]["content"]
        elif "output_text" in resp_json:
            return resp_json["output_text"]
        else:
            print("Respuesta inesperada:", resp_json)
            return "Hubo un error con la IA."
    except Exception as e:
        print("Excepción al llamar a Groq:", e)
        return "Hubo un error con la IA."

# Función que responde mensajes
def responder(update, context):
    texto_usuario = update.message.text
    respuesta = generar_respuesta(texto_usuario)
    update.message.reply_text(respuesta)

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, responder))

# Endpoint webhook para Telegram
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# Inicializar webhook
@app.route("/")
def index():
    return "Bot funcionando"

if __name__ == "__main__":
    # Establecer webhook en Telegram (solo una vez)
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Ej: https://tu-proyecto.up.railway.app/webhook/TOKEN
    if WEBHOOK_URL:
        bot.set_webhook(WEBHOOK_URL)
        print("Webhook establecido en", WEBHOOK_URL)
    app.run(host="0.0.0.0", port=PORT)


