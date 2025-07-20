# features/helpers.py

def predict_direction(symbol, indicators):
    # نموذج بسيط لتوقع الاتجاه
    score = 0
    for indicator in indicators:
        if indicator == "positive":
            score += 1
        elif indicator == "negative":
            score -= 1
    return "up" if score > 0 else "down"


def get_available_symbols():
    # قائمة رموز العملات المتوفرة للتداول
    return ["EURUSD", "USDJPY", "GBPUSD", "BTCUSD", "ETHUSD"]
