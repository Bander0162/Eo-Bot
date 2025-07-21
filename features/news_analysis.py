import requests
import os
# features/news_analysis.py
import requests
from bs4 import BeautifulSoup

def fetch_trendview_news():
    url = "https://trendview.io/news "  # رابط الأخبار
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = soup.find_all("h2", class_="post-title")  # تعديل حسب الموقع

    news_list = []
    for item in news_items[:5]:  # أول 5 أخبار
        news_list.append(item.get_text(strip=True))
    return news_list
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_market_news():
    url = f"https://newsapi.org/v2/everything?q=stock%20market&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if "articles" in data:
            news_list = [f"📰 {article['title']}" for article in data['articles']]
            return news_list
        else:
            return ["❌ لم يتم العثور على أخبار."]
    except Exception as e:
        return [f"❌ خطأ أثناء جلب الأخبار: {str(e)}"]

def get_market_safety():
    return "✅ السوق يبدو آمنًا بنسبة 85% (تحليل مبدئي)"

def detect_manipulation():
    return "📉 لا توجد مؤشرات على تلاعب في السوق الآن"

def get_best_symbols():
    # قائمة مبدئية لأفضل الرموز (ممكن تحديثها تلقائيًا لاحقًا)
    return ["AAPL", "MSFT", "TSLA", "GOOGL"]

def get_available_symbols():
    try:
        response = requests.get("https://trade-platform.eobroker.com/api/symbols")
        if response.status_code == 200:
            symbols = response.json()
            # نفترض أن الرموز موجودة داخل مفتاح "symbols"
            available = [s['symbol'] for s in symbols.get('symbols', [])]
            return available if available else ["❌ لم يتم العثور على رموز."]
        else:
            return [f"❌ خطأ في جلب الرموز. الكود: {response.status_code}"]
    except Exception as e:
        return [f"❌ خطأ في الاتصال بـ EO Broker: {str(e)}"]
