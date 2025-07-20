import os
import telebot
from features import (
    register_account,
    start_auto_trade,
    stop_auto_trade,
    set_trade_settings,
    manual_trade_suggestion,
    get_market_news,
    get_market_safety,
    detect_manipulation,
    get_best_symbols,
    get_available_symbols
)

BOT_TOKEN = os.getenv("
7815435770:AAGXE-Ug3gPT9hG349hg0tUUgyuwaNJFThE")
bot = telebot.TeleBot(BOT_TOKEN)

# ⬇️ تسجيل الحساب في EO Broker
@bot.message_handler(commands=['register'])
def handle_register(message):
    user_id = message.chat.id
    bot.send_message(user_id, "أرسل رمز الدخول (Token) الخاص بك في EO Broker:")
    bot.register_next_step_handler(message, save_token)

user_tokens = {}

def save_token(message):
    user_id = message.chat.id
    token = message.text.strip()
    user_tokens[user_id] = token
    bot.send_message(user_id, "✅ تم حفظ حسابك بنجاح! لن تحتاج لتسجيله مرة أخرى.")

# ⬇️ إعدادات التداول
@bot.message_handler(commands=['set_settings'])
def handle_settings(message):
    user_id = message.chat.id
    bot.send_message(user_id, "كم عدد الصفقات اليومية؟")
    bot.register_next_step_handler(message, get_deals)

def get_deals(message):
    user_id = message.chat.id
    deals = int(message.text.strip())
    bot.send_message(user_id, "نوع رأس المال؟ (full / half / fixed)")
    bot.register_next_step_handler(message, get_capital, deals)

def get_capital(message, deals):
    user_id = message.chat.id
    capital_type = message.text.strip()
    if capital_type == 'fixed':
        bot.send_message(user_id, "أدخل المبلغ الثابت:")
        bot.register_next_step_handler(message, get_fixed_amount, deals, capital_type)
    else:
        get_fixed_amount(message, deals, capital_type, 0)

def get_fixed_amount(message, deals, capital_type, fixed_amount=0):
    user_id = message.chat.id
    if capital_type == 'fixed':
        fixed_amount = float(message.text.strip())
    bot.send_message(user_id, "حدد وقت البداية (مثال: 09:00):")
    bot.register_next_step_handler(message, get_start_time, deals, capital_type, fixed_amount)

def get_start_time(message, deals, capital_type, fixed_amount):
    user_id = message.chat.id
    start_time = message.text.strip()
    bot.send_message(user_id, "حدد وقت النهاية (مثال: 17:00):")
    bot.register_next_step_handler(message, finish_settings, deals, capital_type, fixed_amount, start_time)

def finish_settings(message, deals, capital_type, fixed_amount, start_time):
    user_id = message.chat.id
    end_time = message.text.strip()
    result = set_trade_settings(user_id, deals, capital_type, fixed_amount, start_time, end_time)
    bot.send_message(user_id, result)

# ⬇️ تشغيل التداول التلقائي
@bot.message_handler(commands=['start_auto'])
def handle_start_auto(message):
    user_id = message.chat.id
    result = start_auto_trade(user_id)
    bot.send_message(user_id, result)

# ⬇️ إيقاف التداول التلقائي
@bot.message_handler(commands=['stop_auto'])
def handle_stop_auto(message):
    user_id = message.chat.id
    result = stop_auto_trade(user_id)
    bot.send_message(user_id, result)

# ⬇️ صفقات يدوية
@bot.message_handler(commands=['manual'])
def handle_manual(message):
    user_id = message.chat.id
    suggestion = manual_trade_suggestion()
    bot.send_message(user_id, suggestion)

# ⬇️ عرض الأخبار
@bot.message_handler(commands=['news'])
def handle_news(message):
    news = get_market_news()
    for item in news:
        bot.send_message(message.chat.id, item)

# ⬇️ حالة السوق
@bot.message_handler(commands=['safety'])
def handle_safety(message):
    status = get_market_safety()
    bot.send_message(message.chat.id, status)

# ⬇️ كشف التلاعب
@bot.message_handler(commands=['manipulation'])
def handle_manipulation(message):
    report = detect_manipulation()
    bot.send_message(message.chat.id, report)

# ⬇️ أفضل العملات
@bot.message_handler(commands=['best'])
def handle_best(message):
    best = get_best_symbols()
    bot.send_message(message.chat.id, "🔍 أفضل الأسواق الآن:\n" + "\n".join(best))

# ⬇️ الرموز المتوفرة في EO Broker
@bot.message_handler(commands=['symbols'])
def handle_symbols(message):
    symbols = get_available_symbols()
    bot.send_message(message.chat.id, "💱 الرموز المتاحة:\n" + "\n".join(symbols))

# ⬇️ البداية
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id,
                     "مرحبًا! إليك الأوامر:\n"
                     "/register ➜ تسجيل حسابك\n"
                     "/set_settings ➜ إعدادات التداول\n"
                     "/start_auto ➜ تشغيل التداول\n"
                     "/stop_auto ➜ إيقاف التداول\n"
                     "/manual ➜ صفقة يدوية\n"
                     "/news ➜ أخبار السوق\n"
                     "/safety ➜ حالة السوق\n"
                     "/manipulation ➜ كشف تلاعب\n"
                     "/best ➜ أفضل الأسواق\n"
                     "/symbols ➜ العملات المتاحة")

# ⬇️ تشغيل البوت
if __name__ == '__main__':
    print("✅ البوت يعمل الآن...")
    bot.polling()
