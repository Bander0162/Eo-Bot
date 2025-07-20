import requests
import random

def get_market_news():
    news = [
        "📢 الفيدرالي يعلن رفع الفائدة.",
        "🔥 انخفاض مفاجئ في عملة BTC.",
        "📈 توقعات إيجابية للأسهم الأمريكية.",
        "💥 اضطراب في سوق العملات الرقمية بسبب الأخبار الصينية."
    ]
    return random.choice(news)

def get_market_safety():
    return random.randint(60, 95)

def detect_manipulation(symbol_data):
    if symbol_data["volatility"] > 0.12:
        return True
    return False

def get_best_symbols():
    return [
        {"symbol": "BTCUSDT", "confidence": 90},
        {"symbol": "ETHUSDT", "confidence": 85},
        {"symbol": "SOLUSDT", "confidence": 80}
    ]
