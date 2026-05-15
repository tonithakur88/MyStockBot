import yfinance as yf
import telebot
import os

TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
bot = telebot.TeleBot(TOKEN)

# Stocks list (Isme aap aur bhi add kar sakte hain)
STOCKS = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'TATAMOTORS.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'ITC.NS', 'ZOMATO.NS', 'IRFC.NS'] 

def check_stocks():
    msg = "📊 *Market Scanner Report*\n\n"
    found_any = False
    
    for symbol in STOCKS:
        try:
            # 2 saal ka data le rahe hain taaki ATH aur 200 EMA mil sake
            data = yf.download(symbol, period="2y", interval="1d", progress=False)
            if len(data) < 200: continue
            
            current_price = data['Close'].iloc[-1]
            ema200 = data['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
            ath = data['High'].max()
            atl = data['Low'].min()
            
            # Conditions Check kar rahe hain
            c1 = current_price > ema200  # Condition 1: Above 200 EMA
            c2 = current_price >= (ath * 0.98)  # Condition 2: Near All Time High (2% range)
            c3 = current_price <= (atl * 1.05)  # Condition 3: Near All Time Low (5% range)
            
            conditions_met = []
            if c1: conditions_met.append("🟢 Above 200 EMA")
            if c2: conditions_met.append("🚀 Near All Time High")
            if c3: conditions_met.append("⚠️ Near All Time Low")
            
            # Agar 1 bhi condition puri ho rahi hai toh list mein dalo
            if len(conditions_met) > 0:
                found_any = True
                msg += f"📦 *{symbol}*\n"
                msg += f"💰 Price: {current_price:.2f}\n"
                msg += f"✅ *Met {len(conditions_met)}/3 Conditions:*\n"
                for c in conditions_met:
                    msg += f"  - {c}\n"
                msg += "----------------------------\n"
                
        except Exception as e:
            print(f"Error checking {symbol}: {e}")
            continue
            
    if found_any:
        # Telegram ki limit 4096 characters hoti hai, isliye msg check kar rahe hain
        if len(msg) > 4000:
            bot.send_message(CHAT_ID, "⚠️ Report badi hai, kuch stocks skip ho sakte hain.")
        bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
    else:
        bot.send_message(CHAT_ID, "❌ Aaj koi bhi stock criteria match nahi kar raha.")

if __name__ == "__main__":
    check_stocks()
