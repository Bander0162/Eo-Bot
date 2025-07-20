from features.manual_trade import predict_direction, execute_manual_trade
import random

# العملات المتاحة (منصة EO Broker أو حسب ما يدعمه البوت)
AVAILABLE_SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD"]

# تحديد الاتجاه تلقائياً (كمثال عشوائي أو تحليلي مستقبلاً)
def predict_direction(symbol):
    return random.choice(["up", "down"])

# تنفيذ صفقة يدوية
def execute_manual_trade(user_id, symbol, direction, duration):
    # هنا تقدر ترسل الطلب الحقيقي للمنصة لاحقاً
    return f"✅ صفقة {symbol} ({direction}) لمدة {duration} ثانية تم تنفيذها للمستخدم {user_id}."
