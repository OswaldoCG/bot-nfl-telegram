import os
import logging
from transformers import pipeline
from telegram.ext import Updater, MessageHandler, Filters

# ---------- TOKEN DESDE VARIABLE DE ENTORNO ----------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise SystemExit("ERROR: No existe la variable TOKEN.")

# ---------- LOGGING ----------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------- CARGA DEL MODELO ----------
chatbot = pipeline(
    "text-generation",
    model="distilgpt2"
)

# ---------- FUNCIÓN DE RESPUESTA ----------
def generar_respuesta(texto_usuario: str) -> str:
    prompt = f"Responde como un experto amable en reglas de la NFL. Pregunta: {texto_usuario}"
    salida = chatbot(prompt, max_new_tokens=150)
    texto = salida[0]["generated_text"]
    if "Pregunta:" in texto:
        texto = texto.split("Pregunta:", 1)[-1].strip()
    return texto

def responder(update, context):
    try:
        mensaje = update.message.text
        respuesta = generar_respuesta(mensaje)
        update.message.reply_text("🏈 " + respuesta)
    except Exception as e:
        logger.exception("Error generando respuesta")
        update.message.reply_text("Hubo un error procesando tu mensaje.")

# ---------- INICIO DEL BOT ----------
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, responder))

    logger.info("Bot iniciado y escuchando mensajes...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

