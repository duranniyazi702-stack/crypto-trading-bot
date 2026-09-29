import ccxt
from config import EXCHANGE_NAME, API_KEY, API_SECRET, PAPER_TRADING

class ExchangeHandler:
    def __init__(self):
        self.exchange = getattr(ccxt, EXCHANGE_NAME)({
            "apiKey": API_KEY,
            "secret": API_SECRET,
            "enableRateLimit": True,
            "options": {"defaultType": "spot"}
        }) if not PAPER_TRADING else None
        
        # Paper trading simülasyonu
        self.paper_balance = {"USDT": 1000.0}
        self.paper_trades = []

    def fetch_ohlcv(self, symbol, timeframe, limit=200):
        """OHLCV verisi al"""
        try:
            if PAPER_TRADING:
                return self._mock_ohlcv(symbol, limit)
            return self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        except Exception as e:
            print(f"Error fetching OHLCV: {e}")
            return []

    def _mock_ohlcv(self, symbol, limit):
        """Simülasyon için mock veri"""
        import time
        import random
        data = []
        base_price = 45000
        ts = int(time.time() * 1000)
        
        for i in range(limit):
            change = random.uniform(-2, 2)
            price = base_price + (change * 100)
            data.append([
                ts - (i * 3600000),
                price,
                price + 200,
                price - 200,
                price,
                random.uniform(10, 50)
            ])
        return sorted(data, key=lambda x: x[0])

    def get_balance(self, symbol="USDT"):
        """Bakiye al"""
        try:
            if PAPER_TRADING:
                return self.paper_balance.get(symbol, 0)
            
            balance = self.exchange.fetch_balance()
            return float(balance.get(symbol, {}).get("free", 0))
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return 0.0

    def place_order(self, side, amount, symbol, price=None):
        """Emir ver"""
        try:
            if PAPER_TRADING:
                return self._paper_order(side, amount, symbol, price)
            
            if side.upper() == "BUY":
                order = self.exchange.create_market_buy_order(symbol, amount)
            elif side.upper() == "SELL":
                order = self.exchange.create_market_sell_order(symbol, amount)
            else:
                return False
            
            print(f"Order placed: {order}")
            return True
        except Exception as e:
            print(f"Error placing order: {e}")
            return False

    def _paper_order(self, side, amount, symbol, price):
        """Paper trading simülasyonu"""
        trade = {
            "side": side.upper(),
            "amount": amount,
            "symbol": symbol,
            "price": price,
            "timestamp": __import__('time').time()
        }
        self.paper_trades.append(trade)
        
        base_symbol = symbol.split("/")[0]
        if side.upper() == "BUY":
            cost = amount * price
            self.paper_balance["USDT"] -= cost
            self.paper_balance[base_symbol] = self.paper_balance.get(base_symbol, 0) + amount
        elif side.upper() == "SELL":
            revenue = amount * price
            self.paper_balance["USDT"] += revenue
            self.paper_balance[base_symbol] = self.paper_balance.get(base_symbol, 0) - amount
        
        print(f"[PAPER] {side} {amount} {symbol} @ {price}")
        return True

    def get_position(self, symbol):
        """Pozisyon miktarı al"""
        base_symbol = symbol.split("/")[0]
        return float(self.get_balance(base_symbol))
