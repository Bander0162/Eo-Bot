import os
import telebot
from telebot import types

from features.manual_trade import (
    register_account,
    predict_direction,
    execute_manual_trade,
    get_available_symbols
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# رسالة الترحيب والأزرار
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🧠 أفضل الأسواق", "📉 صفقات يدوية")
    markup.row("✅ إيقاف التداول", "🛑 بدء التداول")
    bot.send_message(message.chat.id, "أهلاً بك! اختر من الأوامر:", reply_markup=markup)

# تسجيل الحساب
@bot.message_handler(commands=['register'])
def handle_register(message):
    result = register_account()
    bot.reply_to(message, result)

# تنفيذ صفقة يدوية
@bot.message_handler(func=lambda msg: msg.text == "📉 صفقات يدوية")
def handle_manual_trade(message):
    symbols = get_available_symbols()
    symbol = random.choice(symbols)
    direction = predict_direction(symbol)
    result = execute_manual_trade(message.chat.id, symbol, direction, 60)
    bot.send_message(message.chat.id, result)

# تشغيل البوت
bot.polling()
