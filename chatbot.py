import os
import requests
from flask import Flask, request
from threading import Thread

# Inicializar Flask
app = Flask(__name__)

# Variables de entorno
TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TOKEN:
    print("ERROR: Falta TOKEN.")
    exit()

if not GROQ_API_KEY:
    print("ERROR: Falta GROQ_API_KEY.")
    exit()

# Función para generar respuesta con Groq
def generar_respuesta(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    # Mensaje de sistema centrado en NFL
    data = {
        "model": "llama-3.1-8b-instant",  # Modelo soportado actualmente
        "messages": [
            {"role": "system", "content": (
                "Eres un experto en NFL. Conoces reglas, jugadores, equipos, estadísticas "
                "y noticias actuales de la liga. Responde de manera clara, precisa y centrada "
                "solo en temas de la NFL, usando un lenguaje amigable para aficionados."
            )},
            {"role": "user", "content": f"{prompt} Responde solo sobre NFL, incluyendo reglas, estadísticas o jugadores si es necesario."}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    r = requests.post(url, headers=headers, json=data)
    try:
        return r.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        print("Error Groq:", r.text)
        return "Hubo un error con la IA."

# Función para procesar mensajes en segundo plano
def procesar_mensaje(data):
    chat_id = data["message"]["chat"]["id"]
    texto_usuario = data["message"]["text"]
    print("Prompt recibido:", texto_usuario)
    respuesta = generar_respuesta(texto_usuario)
    print("Respuesta enviada:", respuesta)
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": respuesta}
    )

# Endpoint del webhook
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        Thread(target=procesar_mensaje, args=(data,)).start()
    return {"ok": True}

# Ejecutar Flask en Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

