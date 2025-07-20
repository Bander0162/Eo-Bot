# تخزين بيانات المستخدمين المسجلين
user_accounts = {}

# تخزين حالة التداول التلقائي
auto_trade_status = {}

# إعدادات الصفقة للمستخدمين
user_settings = {}

# توقيتات التداول
trade_schedule = {}

# تسجيل الحساب
def register_account(user_id, token):
    user_accounts[user_id] = token
    return "✅ تم تسجيل الحساب بنجاح."

# تشغيل التداول التلقائي
def start_auto_trade(user_id):
    auto_trade_status[user_id] = True
    return "✅ تم بدء التداول التلقائي."

# إيقاف التداول التلقائي
def stop_auto_trade(user_id):
    auto_trade_status[user_id] = False
    return "🛑 تم إيقاف التداول التلقائي."

# تحديد إعدادات الصفقة
def set_trade_settings(user_id, deal_count, capital_mode, amount=None):
    user_settings[user_id] = {
        "deals": deal_count,
        "capital": capital_mode,
        "amount": amount
    }
    return "⚙️ تم حفظ إعدادات التداول."

# تحديد أوقات التداول
def set_trade_hours(user_id, start_time, end_time):
    trade_schedule[user_id] = {
        "start": start_time,
        "end": end_time
    }
    return "⏰ تم تعيين وقت التداول بنجاح."
