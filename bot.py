import os
import telebot
from telebot import types

# استيراد الوظائف من ملفات features
from features.manual_trade import predict_direction, get_available_symbols, execute_manual_trade
from features.news_analysis import get_market_news
from features.helpers import register_account, start_auto_trade, stop_auto_trade, set_trade_settings

# إنشاء البوت
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

# شاشة الترحيب
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🗂 أفضل الأسواق", "📈 بدء التداول", "📉 إيقاف التداول")
    markup.row("💡 صفقات يدوية", "🔍 تحليل السوق", "✅ تسجيل الحساب")
    bot.send_message(message.chat.id, "مرحباً بك في بوت التداول 👋", reply_markup=markup)

# تسجيل الحساب
@bot.message_handler(func=lambda m: m.text == "✅ تسجيل الحساب")
def handle_register(message):
    bot.send_message(message.chat.id, "أرسل التوكن الخاص بك:")
    bot.register_next_step_handler(message, save_token)

def save_token(message):
    token = message.text
    user_id = message.from_user.id
    msg = register_account(user_id, token)
    bot.reply_to(message, msg)

# بدء التداول
@bot.message_handler(func=lambda m: m.text == "📈 بدء التداول")
def handle_start_trade(message):
    user_id = message.from_user.id
    msg = start_auto_trade(user_id)
    bot.reply_to(message, msg)

# إيقاف التداول
@bot.message_handler(func=lambda m: m.text == "📉 إيقاف التداول")
def handle_stop_trade(message):
    user_id = message.from_user.id
    msg = stop_auto_trade(user_id)
    bot.reply_to(message, msg)

# تحليل السوق
@bot.message_handler(func=lambda m: m.text == "🔍 تحليل السوق")
def handle_market_analysis(message):
    news = get_market_news()
    bot.reply_to(message, f"📰 تحليل السوق:\n{news}")

# الصفقات اليدوية
@bot.message_handler(func=lambda m: m.text == "💡 صفقات يدوية")
def handle_manual_trade(message):
    symbols = get_available_symbols()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for symbol in symbols:
        markup.row(symbol)
    bot.send_message(message.chat.id, "اختر السوق الذي تريد التداول فيه:", reply_markup=markup)
    bot.register_next_step_handler(message, process_symbol_choice)

def process_symbol_choice(message):
    symbol = message.text
    prediction = predict_direction(symbol)
    msg = f"🔮 التوقع لعملة {symbol} هو: {prediction.upper()}"
    bot.send_message(message.chat.id, msg)

# تشغيل البوت
print("🤖 Bot is running...")
bot.infinity_polling()
