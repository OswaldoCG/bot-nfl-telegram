import os
from transformers import pipeline
from telegram.ext import Updater, MessageHandler, Filters

# -----------------------------
# 1. OBTENER TOKEN DESDE RAILWAY
# -----------------------------
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("ERROR: No existe la variable TOKEN.")
    exit()

# -----------------------------
# 2. CARGAR MODELO LIVIANO SIN TORCH
# -----------------------------
chatbot = pipeline(
    task="text2text-generation",
    model="google/flan-t5-small"
)

# -----------------------------
# 3. FUNCIÓN QUE RESPONDE MENSAJES
# -----------------------------
def responder(update, context):
    texto_usuario = update.message.text

    respuesta = chatbot(
        texto_usuario,
        max_length=60,
        num_return_sequences=1
    )[0]["generated_text"]

    update.message.reply_text(respuesta)

# -----------------------------
# 4. INICIAR EL BOT DE TELEGRAM
# -----------------------------
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.text & ~Filters.command, responder))

print("Bot iniciado y escuchando mensajes...")
updater.start_polling()
updater.idle()



