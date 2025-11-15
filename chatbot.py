import os
import requests
from telegram.ext import Updater, MessageHandler, Filters

# Obtener claves
TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TOKEN:
    print("ERROR: Falta TOKEN.")
    exit()

if not GROQ_API_KEY:
    print("ERROR: Falta GROQ_API_KEY.")
    exit()

# Función para generar texto con Groq
def generar_respuesta(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",   # Modelo rápido y gratuito
        "messages": [
            {"role": "system", "content": "Eres un asistente conversacional amable y útil."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return "Hubo un error con la IA."

    respuesta = response.json()["choices"][0]["message"]["content"]
    return respuesta


# Función que responde mensajes en Telegram
def responder(update, context):
    texto_usuario = update.message.text
    respuesta = generar_respuesta(texto_usuario)
    update.message.reply_text(respuesta)


# Iniciar bot de Telegram
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, responder))

print("Bot IA (Versión 2) iniciado y escuchando mensajes...")
updater.start_polling()
updater.idle()





