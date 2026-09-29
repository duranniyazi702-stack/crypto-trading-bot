import time
import pandas as pd
from datetime import datetime
from exchange_handler import ExchangeHandler
from strategy import Strategy
from config import TRADING_PAIR, TIMEFRAME, TRADE_SIZE_PERCENT, MAX_TRADES_PER_DAY

class TradingBot:
    def __init__(self):
        self.exchange = ExchangeHandler()
        self.strategy = Strategy()
        self.trades_today = 0
        self.last_trade_day = None
        self.running = False
        self.trade_history = []

    def get_ohlcv_dataframe(self):
        """OHLCV verilerini DataFrame'e dönüştür"""
        try:
            candles = self.exchange.fetch_ohlcv(TRADING_PAIR, TIMEFRAME, 200)
            if not candles:
                print("No candle data received")
                return pd.DataFrame()
            
            df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            return df
        except Exception as e:
            print(f"Error getting OHLCV: {e}")
            return pd.DataFrame()

    def execute_trade(self, signal, metrics):
        """Alım-satım işlemini gerçekleştir"""
        try:
            base_symbol = TRADING_PAIR.split("/")[0]
            quote_symbol = TRADING_PAIR.split("/")[1]
            price = metrics.get("price", 0)
            
            if signal == "BUY":
                usdt_balance = self.exchange.get_balance(quote_symbol)
                buy_amount = (usdt_balance * TRADE_SIZE_PERCENT) / price
                
                if buy_amount > 0.001:
                    success = self.exchange.place_order("BUY", buy_amount, TRADING_PAIR, price)
                    if success:
                        trade = {
                            "timestamp": datetime.now(),
                            "side": "BUY",
                            "amount": buy_amount,
                            "price": price,
                            "metrics": metrics
                        }
                        self.trade_history.append(trade)
                        self.trades_today += 1
                        print(f"✓ BUY: {buy_amount:.6f} {base_symbol} @ {price}")
                else:
                    print(f"✗ Insufficient balance for BUY")
            
            elif signal == "SELL":
                coin_balance = self.exchange.get_position(TRADING_PAIR)
                
                if coin_balance > 0.001:
                    success = self.exchange.place_order("SELL", coin_balance, TRADING_PAIR, price)
                    if success:
                        trade = {
                            "timestamp": datetime.now(),
                            "side": "SELL",
                            "amount": coin_balance,
                            "price": price,
                            "metrics": metrics
                        }
                        self.trade_history.append(trade)
                        self.trades_today += 1
                        print(f"✓ SELL: {coin_balance:.6f} {base_symbol} @ {price}")
                else:
                    print(f"✗ No coins to SELL")
        
        except Exception as e:
            print(f"Error executing trade: {e}")

    def print_analysis(self, signal, metrics):
        """Analiz sonuçlarını yazdır"""
        print("\n" + "="*60)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Analysis for {TRADING_PAIR}")
        print("="*60)
        print(f"Price:        {metrics.get('price', 0):.2f}")
        print(f"EMA {EMA_FAST}:         {metrics.get('ema_fast', 0):.2f}")
        print(f"EMA {EMA_SLOW}:        {metrics.get('ema_slow', 0):.2f}")
        print(f"RSI(14):      {metrics.get('rsi', 0):.2f}")
        print(f"BB Upper:     {metrics.get('bb_upper', 0):.2f}")
        print(f"BB Middle:    {metrics.get('bb_middle', 0):.2f}")
        print(f"BB Lower:     {metrics.get('bb_lower', 0):.2f}")
        print(f"MACD:         {metrics.get('macd', 0):.6f}")
        print(f"MACD Signal:  {metrics.get('macd_signal', 0):.6f}")
        print(f"\n>>> SIGNAL: {signal} <<<")
        print(f"Trades today: {self.trades_today}/{MAX_TRADES_PER_DAY}")
        print("="*60 + "\n")

    def reset_daily_counter(self):
        """Günlük sayacı sıfırla"""
        from datetime import date
        today = date.today()
        if self.last_trade_day != today:
            self.trades_today = 0
            self.last_trade_day = today

    def run(self, interval=60):
        """Botu çalıştır"""
        self.running = True
        print("\n" + "="*60)
        print("🤖 TRADING BOT STARTED")
        print(f"Trading Pair: {TRADING_PAIR}")
        print(f"Timeframe: {TIMEFRAME}")
        print(f"Interval: {interval}s")
        print("="*60 + "\n")
        
        try:
            while self.running:
                self.reset_daily_counter()
                
                # Veri al
                df = self.get_ohlcv_dataframe()
                if df.empty:
                    print("Waiting for data...")
                    time.sleep(interval)
                    continue
                
                # Analiz yap
                signal, metrics = self.strategy.analyze(df)
                self.print_analysis(signal, metrics)
                
                # Emir ver
                if self.trades_today < MAX_TRADES_PER_DAY:
                    if signal in ["BUY", "SELL"]:
                        self.execute_trade(signal, metrics)
                else:
                    print(f"Daily trade limit reached ({MAX_TRADES_PER_DAY})")
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\nBot stopped by user.")
            self.stop()
        except Exception as e:
            print(f"Fatal error: {e}")
            self.stop()

    def stop(self):
        """Botu durdur"""
        self.running = False
        print(f"\nBot Summary:")
        print(f"Total trades: {len(self.trade_history)}")
        print(f"USDT balance: {self.exchange.get_balance('USDT'):.2f}")

if __name__ == "__main__":
    bot = TradingBot()
    bot.run(interval=60)  # Her 60 saniyede bir kontrol et
