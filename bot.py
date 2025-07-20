import os
import telebot
from telebot import types

# استيراد الدوال من الملفات داخل مجلد features
from features.manual_trade import (
    register_account,
    start_auto_trade,
    stop_auto_trade,
    set_trade_settings,
    manual_trade_suggestion,
    get_available_symbols
)

from features.news_analysis import (
    get_market_news,
    get_market_safety,
    detect_manipulation,
    get_best_symbols
)

# تهيئة التوكن من متغير البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


# قائمة الأوامر الرئيسية
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📝 التسجيل", "✅ بدء التداول", "🛑 إيقاف التداول")
    markup.row("💡 صفقات يدوية", "📊 أفضل العملات", "📉 نسبة الأمان")
    markup.row("📰 الأخبار", "🔍 العملات المتاحة", "🚨 كشف التلاعب")
    bot.send_message(message.chat.id, "مرحباً بك! اختر من القائمة:", reply_markup=markup)


# أمر التسجيل
@bot.message_handler(func=lambda msg: msg.text == "📝 التسجيل")
def handle_register(message):
    result = register_account()
    bot.send_message(message.chat.id, result)


# بدء التداول التلقائي
@bot.message_handler(func=lambda msg: msg.text == "✅ بدء التداول")
def handle_start_trade(message):
    result = start_auto_trade()
    bot.send_message(message.chat.id, result)


# إيقاف التداول التلقائي
@bot.message_handler(func=lambda msg: msg.text == "🛑 إيقاف التداول")
def handle_stop_trade(message):
    result = stop_auto_trade()
    bot.send_message(message.chat.id, result)


# التداول اليدوي
@bot.message_handler(func=lambda msg: msg.text == "💡 صفقات يدوية")
def handle_manual_trade(message):
    result = manual_trade_suggestion()
    bot.send_message(message.chat.id, result)


# عرض العملات المناسبة للتداول
@bot.message_handler(func=lambda msg: msg.text == "📊 أفضل العملات")
def handle_best_symbols(message):
    result = get_best_symbols()
    bot.send_message(message.chat.id, result)


# عرض نسبة الأمان السوقي
@bot.message_handler(func=lambda msg: msg.text == "📉 نسبة الأمان")
def handle_market_safety(message):
    result = get_market_safety()
    bot.send_message(message.chat.id, result)


# كشف التلاعب في السوق
@bot.message_handler(func=lambda msg: msg.text == "🚨 كشف التلاعب")
def handle_manipulation(message):
    result = detect_manipulation()
    bot.send_message(message.chat.id, result)


# عرض الأخبار الاقتصادية
@bot.message_handler(func=lambda msg: msg.text == "📰 الأخبار")
def handle_market_news(message):
    result = get_market_news()
    bot.send_message(message.chat.id, result)


# العملات المتاحة في المنصة
@bot.message_handler(func=lambda msg: msg.text == "🔍 العملات المتاحة")
def handle_symbols(message):
    result = get_available_symbols()
    bot.send_message(message.chat.id, result)


# التشغيل
bot.polling()
