import random

def get_available_symbols():
    return ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "LTCUSDT"]

def analyze_manual_trade(symbol):
    direction = random.choice(["⬆️ صعود", "⬇️ نزول"])
    duration = random.choice(["3 دقائق", "5 دقائق", "10 دقائق"])
    confidence = random.randint(70, 95)
    
    return {
        "symbol": symbol,
        "direction": direction,
        "duration": duration,
        "confidence": confidence
    }
