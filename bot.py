import yfinance as yf
import telebot
import os
from datetime import datetime

TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
bot = telebot.TeleBot(TOKEN)

# Tere 200+ stocks ki list
STOCKS = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'INFY.NS', 'BHARTIARTL.NS', 'ITC.NS', 'SBIN.NS', 'LICI.NS', 'HINDUNILVR.NS',
    'LT.NS', 'BAJFINANCE.NS', 'HCLTECH.NS', 'MARUTI.NS', 'SUNPHARMA.NS', 'ADANIENT.NS', 'TATAMOTORS.NS', 'TITAN.NS', 'ONGC.NS', 'NTPC.NS',
    'AXISBANK.NS', 'KOTAKBANK.NS', 'ADANIPORTS.NS', 'ULTRACEMCO.NS', 'ASIANPAINT.NS', 'COALINDIA.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'M&M.NS', 'GRASIM.NS',
    'NESTLEIND.NS', 'JSWSTEEL.NS', 'ADANIPOWER.NS', 'TATASTEEL.NS', 'HINDALCO.NS', 'POWERGRID.NS', 'SBILIFE.NS', 'LTIM.NS', 'DIVISLAB.NS', 'TATACONSUM.NS',
    'BAJAJ-AUTO.NS', 'BRITANNIA.NS', 'WIPRO.NS', 'EICHERMOT.NS', 'HDFCLIFE.NS', 'DRREDDY.NS', 'APOLLOHOSP.NS', 'CIPLA.NS', 'HEROMOTOCO.NS', 'TECHM.NS',
    'JIOFIN.NS', 'ZOMATO.NS', 'HAL.NS', 'CANBK.NS', 'IDFCFIRSTB.NS', 'PNB.NS', 'BOB.NS', 'UNIONBANK.NS', 'IRFC.NS', 'RVNL.NS',
    'RECLTD.NS', 'PFC.NS', 'BEL.NS', 'GAIL.NS', 'DLF.NS', 'VBL.NS', 'SIEMENS.NS', 'ABB.NS', 'TRENT.NS', 'CHOLAFIN.NS',
    'TVSMOTOR.NS', 'POLYCAB.NS', 'LODHA.NS', 'AUROPHARMA.NS', 'MAHABANK.NS', 'INDIANB.NS', 'YESBANK.NS', 'UCOBANK.NS', 'CENTRALBK.NS', 'IOB.NS',
    'NHPC.NS', 'SJVN.NS', 'MAHINDCIE.NS', 'TATACOMM.NS', 'PETRONET.NS', 'MANAPPURAM.NS', 'MUTHOOTFIN.NS', 'ABCAPITAL.NS', 'BANDHANBNK.NS', 'FEDERALBNK.NS',
    'IDFC.NS', 'GMRINFRA.NS', 'SUZLON.NS', 'IDEA.NS', 'ASHOKLEY.NS', 'CUMMINSIND.IND.NS', 'BERGEPAINT.NS', 'PIDILITIND.NS', 'BATAINDIA.NS', 'RELAXO.NS',
    'HAVELLS.NS', 'VOLTAS.NS', 'ASTRAL.NS', 'KEI.NS', 'SUPREMEIND.NS', 'DIXON.NS', 'KPITTECH.NS', 'PERSISTENT.NS', 'COFORGE.NS', 'MPHASIS.NS',
    'TATAELXSI.NS', 'LTTS.NS', 'OBEROIRLTY.NS', 'PHOENIXLTD.NS', 'PRESTIGE.NS', 'BRIGADE.NS', 'SOBHA.NS', 'JUBLFOOD.NS', 'DEVYANI.NS', 'SAPPHIRE.NS',
    'NYKAA.NS', 'PAYTM.NS', 'POLICYBZR.NS', 'DELHIVERY.NS', 'CARBORUNIV.NS', 'CHAMBLFERT.NS', 'COROMANDEL.NS', 'DEEPAKNTR.NS', 'GNFC.NS', 'GSFC.NS',
    'NAVINFLUOR.NS', 'SRF.NS', 'TATACHEM.NS', 'UPL.NS', 'PIIND.NS', 'CONCOR.NS', 'EXIDEIND.NS', 'AMBUJACEM.NS', 'ACC.NS', 'JKCEMENT.NS',
    'SHREECEM.NS', 'DALBHARAT.NS', 'RAMCOCEM.NS', 'AUBANK.NS', 'ESCORTS.NS', 'BALKRISIND.NS', 'BHARATFORG.NS', 'MRF.NS', 'APOLLOTYRE.NS', 'JKTYRE.NS',
    'CEATLTD.NS', 'TATAINVEST.NS', 'HUDCO.NS', 'IREDA.NS', 'GICRE.NS', 'NIACL.NS', 'HDFCAMC.NS', 'NAM-INDIA.NS', 'BSE.NS', 'MCX.NS',
    'IEX.NS', 'CDSL.NS', 'KIMS.NS', 'MAXHEALTH.NS', 'FORTIS.NS', 'GLOBAL.NS', 'METROPOLIS.NS', 'LALPATHLAB.NS', 'SYNGENE.NS', 'IPCALAB.NS',
    'GLAND.NS', 'LAURUSLABS.NS', 'BIOCON.NS', 'ALKEM.NS', 'GLENMARK.NS', 'ABBOTINDIA.NS', 'JBCHEPHARM.NS', 'ALKYLAMINE.NS', 'FLUOROCHEM.NS', 'VINATIORGA.NS',
    'AETHER.NS', 'CLEAN.NS', 'TATAPOWER.NS', 'JSWENERGY.NS', 'CESC.NS', 'MAZDOCK.NS', 'GRSE.NS', 'BDL.NS', 'BEML.NS', 'COCHINSHIP.NS',
    'L&TFH.NS', 'MFSL.NS', 'PEL.NS', 'POONAWALLA.NS', 'CREDITACC.NS', 'MSUMI.NS', 'SONACOMS.NS', 'TIINDIA.NS', 'UNOMINDA.NS', 'ENDURANCE.NS'
]

def get_market_mood():
    try:
        nifty = yf.download('^NSEI', period='2d', progress=False)
        prev_close = nifty['Close'].iloc[-2]
        curr_price = nifty['Close'].iloc[-1]
        diff = curr_price - prev_close
        pct = (diff / prev_close) * 100
        
        mood = " Bullish" if diff > 0 else " Bearish"
        emoji = "📈" if diff > 0 else "📉"
        return f"{emoji} *Nifty 50 Mood:* {mood} ({diff:+.2f} pts | {pct:+.2f}%)\n"
    except:
        return "⚠️ Nifty data nahi mil paya.\n"

def check_stocks():
    msg = get_market_mood()
    msg += f"⏰ *Scan Time:* {datetime.now().strftime('%I:%M %p')}\n"
    msg += "----------------------------\n\n"
    found_any = False
    
    for symbol in STOCKS:
        try:
            data = yf.download(symbol, period="2y", interval="1d", progress=False)
            if len(data) < 200: continue
            
            current_price = data['Close'].iloc[-1]
            ema200 = data['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
            ath = data['High'].max()
            atl = data['Low'].min()
            
            # Nayi Condition: 200 EMA ke 3% ke डेयर (Range) mein hai ya nahi
            ema_upper_limit = ema200 * 1.03
            ema_lower_limit = ema200 * 0.97
            
            c1 = current_price > ema200
            c2 = current_price >= (ath * 0.98)
            c3 = current_price <= (atl * 1.05)
            c4 = ema_lower_limit <= current_price <= ema_upper_limit # Near 200 EMA
            
            conditions_met = []
            if c1: conditions_met.append("🟢 Above 200 EMA")
            if c2: conditions_met.append("🚀 Near All Time High")
            if c3: conditions_met.append("⚠️ Near All Time Low")
            if c4: conditions_met.append("🎯 Near 200 EMA Support/Resistance (3% Range)")
            
            if len(conditions_met) > 0:
                found_any = True
                msg += f"📦 *{symbol.split('.')[0]}* | Price: {current_price:.2f}\n"
                for c in conditions_met:
                    msg += f"  - {c}\n"
                msg += "----------------------------\n"
                
        except:
            continue
            
    if found_any:
        # Agar message bahut bada ho jaye toh parts mein bhejenge
        if len(msg) > 4000:
            for i in range(0, len(msg), 4000):
                bot.send_message(CHAT_ID, msg[i:i+4000], parse_mode='Markdown')
        else:
            bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
    else:
        bot.send_message(CHAT_ID, "❌ Koi stock match nahi hua.")

if __name__ == "__main__":
    check_stocks()
