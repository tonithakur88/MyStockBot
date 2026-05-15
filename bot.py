import yfinance as yf
import telebot
import os

# Telegram details (Hum isse safe rakhenge baad mein)
TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
bot = telebot.TeleBot(TOKEN)

# Stocks list (Nifty 50 ya 100 ke tickers)
STOCKS = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'TATAMOTORS.NS', 'SBIN.NS', 'BHARTIARTL.NS'] 

def check_stocks():
    msg = "🚀 *Stocks Above 200 EMA & Near ATH:*\n\n"
    found = False
    
    for symbol in STOCKS:
        try:
            data = yf.download(symbol, period="2y", interval="1d", progress=False)
            if len(data) < 200: continue
            
            current_price = data['Close'].iloc[-1]
            ema200 = data['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
            ath = data['High'].max()
            
            # Condition: Price 200 EMA ke upar aur ATH ke 2% paas
            if current_price > ema200 and current_price >= (ath * 0.98):
                msg += f"✅ *{symbol}*\nPrice: {current_price:.2f} | ATH: {ath:.2f}\n\n"
                found = True
        except:
            continue
            
    if found:
        bot.send_message(CHAT_ID, msg, parse_mode='Markdown')

if __name__ == "__main__":
    check_stocks()
