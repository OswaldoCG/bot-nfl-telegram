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
    # Cambia este URL por el endpoint exacto de tu modelo en tu dashboard de Groq
    url = "https://api.groq.com/openai/v1"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
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

        respuesta = response.json()
        # Dependiendo de la estructura del endpoint, puede ser:
        # respuesta["choices"][0]["message"]["content"]
        # o respuesta["output_text"] (revisa tu dashboard de Groq)
        if "choices" in respuesta:
            return respuesta["choices"][0]["message"]["content"]
        elif "output_text" in respuesta:
            return respuesta["output_text"]
        else:
            print("Respuesta inesperada:", respuesta)
            return "Hubo un error con la IA."

    except Exception as e:
        print("Excepción al llamar a Groq:", e)
        return "Hubo un error con la IA."

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

