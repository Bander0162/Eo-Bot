from features.manual_trade import predict_direction, execute_manual_trade
import os
import telebot
from telebot import types
from features import register_account, start_auto_trade, stop_auto_trade, set_trade_settings
from features.news_analysis import get_market_news, get_market_safety, detect_manipulation, get_best_symbols
from features.manual_trade import get_available_symbols, analyze_manual_trade

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📰 الأخبار", "📊 حالة السوق", "📈 أفضل الأسواق")
    markup.row("🔍 كشف التلاعب", "💡 صفقات يدوية")
    markup.row("✅ بدء التداول", "🛑 إيقاف التداول")
    bot.send_message(message.chat.id, "مرحباً بك في بوت التداول 👋", reply_markup=markup)

@bot.message_handler(commands=['register'])
def handle_register(message):
    user_id = message.chat.id
    token = "YOUR_EO_BROKER_TOKEN"  # يمكن تغييره لاحقاً
    result = register_account(user_id, token)
    bot.send_message(user_id, result)

@bot.message_handler(commands=['set_settings'])
def handle_settings(message):
    user_id = message.chat.id
    result = set_trade_settings(user_id, 3, 'half', 50, '09:00', '17:00')
    bot.send_message(user_id, result)

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    user_id = message.chat.id
    if message.text == "📰 الأخبار":
        news = get_market_news()
        bot.send_message(user_id, f"🗞️ {news}")

    elif message.text == "📊 حالة السوق":
        safety = get_market_safety()
        bot.send_message(user_id, f"📊 نسبة أمان السوق: {safety}%")

    elif message.text == "📈 أفضل الأسواق":
        best = get_best_symbols()
        msg = "✅ أفضل الأسواق:\n" + "\n".join(f"• {s['symbol']} - {s['confidence']}%" for s in best)
        bot.send_message(user_id, msg)

    elif message.text == "🔍 كشف التلاعب":
        data = {"volatility": 0.18}  # مثال وهمي
        if detect_manipulation(data):
            bot.send_message(user_id, "⚠️ السوق فيه تلاعب! الخروج الآن.")
        else:
            bot.send_message(user_id, "✅ السوق مستقر حالياً.")

    elif message.text == "💡 صفقات يدوية":
        symbols = get_available_symbols()
        markup = types.InlineKeyboardMarkup()
        for sym in symbols:
            markup.add(types.InlineKeyboardButton(sym, callback_data=f"manual_{sym}"))
        bot.send_message(user_id, "اختر عملة لتحليلها:", reply_markup=markup)

    elif message.text == "✅ بدء التداول":
        result = start_auto_trade(user_id)
        bot.send_message(user_id, result)

    elif message.text == "🛑 إيقاف التداول":
        result = stop_auto_trade(user_id)
        bot.send_message(user_id, result)

@bot.callback_query_handler(func=lambda call: call.data.startswith("manual_"))
def handle_manual_trade(call):
    symbol = call.data.replace("manual_", "")
    result = analyze_manual_trade(symbol)
    msg = f"💡 تحليل {symbol}:\nالاتجاه: {result['direction']}\nالمدة: {result['duration']}\nالثقة: {result['confidence']}%"
    bot.send_message(call.message.chat.id, msg)

bot.infinity_polling()
@bot.message_handler(commands=["manual_trade"])
def manual_trade_handler(message):
    user_id = message.chat.id
    symbols = ["EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD"]
    
    # إعداد قائمة أزرار
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for symbol in symbols:
        markup.add(types.KeyboardButton(symbol))

    bot.send_message(user_id, "📌 اختر العملة التي تريد التداول عليها:", reply_markup=markup)

    bot.register_next_step_handler(message, process_symbol_selection)

def process_symbol_selection(message):
    user_id = message.chat.id
    symbol = message.text.strip().upper()
    
    direction = predict_direction(symbol)
    duration = 60  # تقدر تخلي المستخدم يحددها لاحقاً
    
    result = execute_manual_trade(user_id, symbol, direction, duration)
    
    bot.send_message(user_id, f"🚀 الاتجاه المتوقع: {direction.upper()}")
    bot.send_message(user_id, result)
