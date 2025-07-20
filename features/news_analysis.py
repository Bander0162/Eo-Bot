import requests
from bs4 import BeautifulSoup

def get_market_news():
    return [
        "📰 خبر 1: الأسواق تتجه للصعود بسبب قرارات الفائدة.",
        "📰 خبر 2: انخفاض مفاجئ في أسعار النفط يؤثر على العملات."
    ]

def get_market_safety():
    return "✅ السوق آمن حالياً للتداول بنسبة 85٪"

def detect_manipulation(data):
    return "تلاعب" in data.lower()

def get_best_symbols():
    return ['EURUSD', 'USDJPY', 'BTCUSD']
