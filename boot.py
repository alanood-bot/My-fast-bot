import ccxt
import pandas as pd
import pandas_ta as ta
import time
import requests
from datetime import datetime
import warnings

# إلغاء كافة التحذيرات التي تسبب تجمد الشاشة السوداء
warnings.filterwarnings("ignore")

TOKEN = "8389783870:AAHpZkfuEjUF7Nhd7bUyPVovLc24DPr81qI"
CHAT_ID = "-1002331987595"

# قائمة مختارة لأقوى 20 عملة (لضمان عدم توقف الحساب المجاني)
SYMBOLS = [
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT', 
    'ADA/USDT', 'DOGE/USDT', 'AVAX/USDT', 'DOT/USDT', 'LINK/USDT',
    'MATIC/USDT', 'NEAR/USDT', 'SHIB/USDT', 'LTC/USDT', 'FET/USDT',
    'SUI/USDT', 'PEPE/USDT', 'WIF/USDT', 'BONK/USDT', 'FLOKI/USDT'
]

exchange = ccxt.binance({'enableRateLimit': True})

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def get_signals():
    print(f"✅ فحص آمن جاري الآن... {datetime.now().strftime('%H:%M:%S')}")
    for symbol in SYMBOLS:
        try:
            # طلب بيانات أقل (30 شمعة فقط) لتوفير جهد المعالج
            bars = exchange.fetch_ohlcv(symbol, timeframe='5m', limit=30)
            df = pd.DataFrame(bars, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
            df['RSI'] = ta.rsi(df['c'], length=14)
            
            last = df.iloc[-1]
            price = last['c']
            coin = symbol.split('/')[0]
            rsi_val = last['RSI']

            if rsi_val < 40: # دخول شراء
                tp = price * 1.015
                msg = f"🦁 *إشارة VIP (LONG)*\n🪙 #{coin}\n💰 السعر: `{price}`\n📊 RSI: `{rsi_val:.2f}`\n🎯 الهدف: `{tp:.4f}`"
                send_msg(msg)
                time.sleep(2) # راحة قصيرة بين الإرسال والآخر

            elif rsi_val > 60: # دخول بيع
                tp = price * 0.985
                msg = f"🦁 *إشارة VIP (SHORT)*\n🪙 #{coin}\n💰 السعر: `{price}`\n📊 RSI: `{rsi_val:.2f}`\n🎯 الهدف: `{tp:.4f}`"
                send_msg(msg)
                time.sleep(2)
        except: continue

# انطلاق
send_msg("✨ *تم تشغيل النسخة الاقتصادية*\nالبوت يعمل الآن بنظام الفحص الآمن المستمر...")

while True:
    get_signals()
    # انتظار لمدة 5 دقائق بين كل دورة فحص كاملة لتوفير الـ CPU
    time.sleep(300) 
