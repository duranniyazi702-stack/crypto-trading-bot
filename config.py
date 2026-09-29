import os
from dotenv import load_dotenv

load_dotenv()

# Exchange Settings
EXCHANGE_NAME = "binance"
TRADING_PAIR = os.getenv("TRADING_PAIR", "BTC/USDT")
TIMEFRAME = os.getenv("TIMEFRAME", "1h")
LOOKBACK = 200

# API Credentials
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Strategy Parameters
BUY_RSI = float(os.getenv("BUY_RSI", 45))
SELL_RSI = float(os.getenv("SELL_RSI", 70))
EMA_FAST = int(os.getenv("EMA_FAST", 9))
EMA_SLOW = int(os.getenv("EMA_SLOW", 21))

# Paper Trading
PAPER_TRADING = os.getenv("PAPER_TRADING", "True").lower() == "true"

# Trading Parameters
TRADE_SIZE_PERCENT = 0.2  # Her alımda bakiyenin %20'si
MAX_TRADES_PER_DAY = 10

# Flask Settings
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
