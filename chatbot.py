import os
from telegram.ext import Updater, MessageHandler, Filters

# 1) Obtener TOKEN desde Railway
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("ERROR: No existe la variable TOKEN.")
    exit()

# 2) Función que responde a cada mensaje
def responder(update, context):
    usuario = update.message.from_user.first_name
    texto = update.message.text

    respuesta = f"Hola {usuario}! Dijiste: {texto}\nEsta es la versión 1 del bot, funcionando 24/7."
    
    update.message.reply_text(respuesta)

# 3) Inicializar bot
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# 4) Manejar mensajes
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, responder))

print("Bot iniciado (Versión 1) y escuchando mensajes...")
updater.start_polling()
updater.idle()



