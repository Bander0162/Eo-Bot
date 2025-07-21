# تحديد عدد الصفقات اليومية
MAX_TRADES = 20 # الحد الأقصى من الصفقات
trade_count = 0  # العداد

def can_open_trade():
    global trade_count
    if trade_count < MAX_TRADES:
        return True
    else:
        return False

def increment_trade():
    global trade_count
    if can_open_trade():
        trade_count += 1
        return True
    else:
        return False

def reset_trades():
    global trade_count
    trade_count = 0
