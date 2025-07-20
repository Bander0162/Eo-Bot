from features.helpers import predict_direction, get_available_symbols
import random

# العملات المتاحة حسب منصة EO Broker
AVAILABLE_SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD"]

# توقع الاتجاه (عشوائي أو من التحليل الفني لاحقًا)
def predict_direction(symbol):
    return random.choice(["up", "down"])

# تنفيذ صفقة يدوية
def execute_manual_trade(user_id, symbol, direction, duration):
    # هنا مستقبلاً ترسل الطلب الحقيقي لـ EO Broker
    return f"✅ تم تنفيذ الصفقة للمستخدم {user_id} على {symbol} باتجاه {direction} لمدة {duration} ثانية"

# جلب العملات المتاحة (يمكنك تطويرها لاحقاً لتكون ديناميكية من API)
def get_available_symbols():
    return AVAILABLE_SYMBOLS

# تسجيل الحساب (بشكل مبسط حالياً)
def register_account():
    return "✅ تم تسجيل الحساب بنجاح!"
