from keep_alive import keep_alive
import os
import telebot
from telebot import types
from features.manual_trade import (
    get_available_symbols,
    predict_direction,
    execute_manual_trade
)
from features.news_analysis import (
    get_market_news,
    get_market_safety,
    detect_manipulation,
    get_best_symbols
)
from features.helpers import (
    register_account,
    start_auto_trade,
    stop_auto_trade,
    set_trade_settings
)
from features.trade_limits import can_open_trade, increment_trade

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# قائمة الأوامر الرئيسية
@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📈 تشغيل التداول التلقائي"),
        types.KeyboardButton("📉 إيقاف التداول"),
        types.KeyboardButton("✍️ صفقات يدوية"),
        types.KeyboardButton("🧠 أفضل الأسواق"),
        types.KeyboardButton("📊 تحليلات السوق"),
        types.KeyboardButton("🚨 مراقبة التلاعب"),
        types.KeyboardButton("⏱️ وقت التداول"),
        types.KeyboardButton("💰 نوع رأس المال")
    )
    bot.send_message(message.chat.id, "أهلاً بك! اختر من الأوامر:", reply_markup=markup)

# تشغيل التداول التلقائي
@bot.message_handler(func=lambda msg: msg.text == "📈 تشغيل التداول التلقائي")
def handle_auto_trade(message):
    response = start_auto_trade(message.from_user.id)
    bot.reply_to(message, f"✅ تم بدء التداول التلقائي: {response}")

# إيقاف التداول
@bot.message_handler(func=lambda msg: msg.text == "📉 إيقاف التداول")
def handle_stop_trade(message):
    response = stop_auto_trade(message.from_user.id)
    bot.reply_to(message, f"🛑 تم إيقاف التداول: {response}")

# صفقات يدوية
@bot.message_handler(func=lambda msg: msg.text == "✍️ صفقات يدوية")
def handle_manual_trade(message):
    symbols = get_available_symbols()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for sym in symbols:
        markup.add(types.KeyboardButton(sym))
    bot.send_message(message.chat.id, "اختر العملة للتداول اليدوي:", reply_markup=markup)

# اختيار العملة لتداول يدوي
@bot.message_handler(func=lambda msg: msg.text in get_available_symbols())
def handle_symbol_selected(message):
    symbol = message.text
    direction = predict_direction(symbol)
    bot.send_message(
        message.chat.id,
        f"🔮 التوقع: {symbol} سيذهب إلى الأعلى أو الأسفل: {direction}\n\nاكتب المدة (بالثواني) للتداول:"
    )
    bot.register_next_step_handler(message, lambda m: execute_manual(message, symbol, direction, m.text))

def execute_manual(message, symbol, direction, duration):
    try:
        seconds = int(duration)
        result = execute_manual_trade(message.from_user.id, symbol, direction, seconds)
        bot.send_message(message.chat.id, result)
    except:
        bot.send_message(message.chat.id, "❌ صيغة غير صحيحة، يرجى إرسال رقم المدة بالثواني.")

# أفضل الأسواق
@bot.message_handler(func=lambda msg: msg.text == "🧠 أفضل الأسواق")
def handle_best_symbols(message):
    result = get_best_symbols()
    bot.send_message(message.chat.id, f"📈 أفضل الأسواق حالياً:\n{result}")

# تحليلات السوق
@bot.message_handler(func=lambda msg: msg.text == "📊 تحليلات السوق")
def handle_market_news(message):
    result = get_market_news()
    bot.send_message(message.chat.id, f"📰 آخر الأخبار:\n{result}")

# مراقبة التلاعب
@bot.message_handler(func=lambda msg: msg.text == "🚨 مراقبة التلاعب")
def handle_manipulation(message):
    result = detect_manipulation()
    bot.send_message(message.chat.id, f"🚨 تحليل التلاعب:\n{result}")

# وقت التداول
@bot.message_handler(func=lambda msg: msg.text == "⏱️ وقت التداول")
def handle_time_setting(message):
    bot.send_message(message.chat.id, "🕒 أرسل وقت البداية والنهاية هكذا:\nمثال: 09:00-15:30")
    bot.register_next_step_handler(message, save_time_range)

def save_time_range(message):
    try:
        start, end = message.text.split("-")
        response = set_trade_settings("time_range", {"start": start, "end": end})
        bot.send_message(message.chat.id, f"✅ تم تعيين وقت التداول من {start} إلى {end}")
    except:
        bot.send_message(message.chat.id, "❌ تأكد من كتابة الوقت بشكل صحيح (مثال: 08:30-16:00)")

# نوع رأس المال
@bot.message_handler(func=lambda msg: msg.text == "💰 نوع رأس المال")
def handle_capital_type(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("كامل", "نصف", "مبلغ ثابت")
    bot.send_message(message.chat.id, "اختر نوع رأس المال:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text in ["كامل", "نصف", "مبلغ ثابت"])
def save_capital_type(message):
    response = set_trade_settings("capital_type", message.text)
    bot.send_message(message.chat.id, f"✅ تم تعيين نوع رأس المال: {message.text}")

keep_alive()
# تشغيل البوت
bot.infinity_polling()
