
import telegram
from telegram.ext import Updater, CommandHandler
import os

def start(update, context):
    update.message.reply_text("تم تشغيل البوت ✅")

def stop(update, context):
    update.message.reply_text("تم إيقاف البوت ❌")

updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("stop", stop))

updater.start_polling()
