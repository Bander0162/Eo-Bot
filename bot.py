import os
import telebot
from telebot import types

# استيراد الوظائف من ملفات features
from features.manual_trade import predict_direction, get_available_symbols
from features.news_analysis import get_market_news, get_market_safety, detect_manipulation, get_best_symbols
from features import register_account, start_auto_trade, stop_auto_trade, set_trade_settings

# تهيئة البوت باستخدام توكن البيئة
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

# رسالة الترحيب + قائمة الأزرار الرئيسية
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📰 أفضل الأسواق 📈", "⚠️ حالة السوق")
    markup.row("💡 صفقات يدوية 🔍", "📊 تحليل الأخبار")
    markup.row("✅ بدء التداول", "⛔️ إيقاف التداول")
    bot.send_message(message.chat.id, "مرحباً بك! 👋\nاختر من الأزرار التالية:", reply_markup=markup)

# تسجيل الحساب في البوت
@bot.message_handler(commands=['register'])
def handle_register(message):
    try:
        user_id = message.chat.id
        token = message.text.split()[1]
        result = register_account(user_id, token)
        bot.send_message(user_id, result)
    except IndexError:
        bot.send_message(message.chat.id, "❌ استخدم الأمر بهذا الشكل:\n/register <token>")

# بدء التداول التلقائي
@bot.message_handler(func=lambda msg: msg.text == "✅ بدء التداول")
def handle_start_trade(message):
    result = start_auto_trade(message.chat.id)
    bot.send_message(message.chat.id, result)

# إيقاف التداول التلقائي
@bot.message_handler(func=lambda msg: msg.text == "⛔️ إيقاف التداول")
def handle_stop_trade(message):
    result = stop_auto_trade(message.chat.id)
    bot.send_message(message.chat.id, result)

# عرض أفضل الأسواق
@bot.message_handler(func=lambda msg: msg.text == "📰 أفضل الأسواق 📈")
def handle_best_symbols(message):
    best = get_best_symbols()
    bot.send_message(message.chat.id, "📈 أفضل الأسواق:\n" + "\n".join(best))

# عرض تحليل الأخبار
@bot.message_handler(func=lambda msg: msg.text == "📊 تحليل الأخبار")
def handle_news_analysis(message):
    analysis = get_market_news()
    bot.send_message(message.chat.id, f"📰 تحليل الأخبار:\n{analysis}")

# عرض حالة السوق الحالية (النسبة المئوية للأمان)
@bot.message_handler(func=lambda msg: msg.text == "⚠️ حالة السوق")
def handle_market_safety(message):
    safety = get_market_safety()
    bot.send_message(message.chat.id, f"⚠️ نسبة أمان السوق الحالية: {safety}%")

# تنبؤ يدوي: اختيار زوج عملات والحصول على الاتجاه المتوقع
@bot.message_handler(func=lambda msg: msg.text == "💡 صفقات يدوية 🔍")
def handle_manual_trade(message):
    symbols = get_available_symbols()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for symbol in symbols:
        markup.row(symbol)
    bot.send_message(message.chat.id, "🔍 اختر زوج العملات:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text in get_available_symbols())
def handle_symbol_prediction(message):
    direction = predict_direction(message.text)
    bot.send_message(message.chat.id, f"🔮 الاتجاه المتوقع لـ {message.text} هو: {direction}")

# كشف التلاعب في السوق
@bot.message_handler(commands=['detect'])
def handle_detect(message):
    report = detect_manipulation()
    bot.send_message(message.chat.id, f"🛑 تقرير التلاعب:\n{report}")

# تشغيل البوت
bot.polling()
