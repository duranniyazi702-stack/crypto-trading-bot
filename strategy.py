import pandas as pd
import numpy as np
from config import BUY_RSI, SELL_RSI, EMA_FAST, EMA_SLOW

class Strategy:
    def __init__(self):
        self.last_signal = "HOLD"
        self.buy_price = 0
        self.sell_price = 0

    @staticmethod
    def ema(series, period):
        """Exponential Moving Average"""
        return series.ewm(span=period, adjust=False).mean()

    @staticmethod
    def rsi(series, period=14):
        """Relative Strength Index"""
        delta = series.diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ma_up = up.ewm(com=period - 1, adjust=False, min_periods=period).mean()
        ma_down = down.ewm(com=period - 1, adjust=False, min_periods=period).mean()
        rs = ma_up / ma_down
        return 100 - (100 / (1 + rs))

    @staticmethod
    def bollinger_bands(series, period=20, std_dev=2):
        """Bollinger Bands"""
        sma = series.rolling(period).mean()
        std = series.rolling(period).std()
        upper = sma + (std * std_dev)
        lower = sma - (std * std_dev)
        return upper, sma, lower

    @staticmethod
    def macd(series, fast=12, slow=26, signal=9):
        """MACD Indicator"""
        ema_fast = series.ewm(span=fast).mean()
        ema_slow = series.ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    def analyze(self, df):
        """Ana analiz fonksiyonu"""
        if df.empty or len(df) < 30:
            return "HOLD", {"error": "Yetersiz veri"}

        close = df["close"]
        
        # Göstergeleri hesapla
        ema_fast_val = self.ema(close, EMA_FAST).iloc[-1]
        ema_slow_val = self.ema(close, EMA_SLOW).iloc[-1]
        rsi_val = self.rsi(close, 14).iloc[-1]
        
        upper_bb, middle_bb, lower_bb = self.bollinger_bands(close)
        macd_line, signal_line, histogram = self.macd(close)
        
        price = close.iloc[-1]
        
        # Analiz metrikleri
        metrics = {
            "price": float(price),
            "ema_fast": float(ema_fast_val),
            "ema_slow": float(ema_slow_val),
            "rsi": float(rsi_val),
            "bb_upper": float(upper_bb.iloc[-1]),
            "bb_middle": float(middle_bb.iloc[-1]),
            "bb_lower": float(lower_bb.iloc[-1]),
            "macd": float(macd_line.iloc[-1]),
            "macd_signal": float(signal_line.iloc[-1]),
            "macd_histogram": float(histogram.iloc[-1])
        }
        
        # Sinyal üret
        signal = self._generate_signal(ema_fast_val, ema_slow_val, rsi_val, 
                                       macd_line.iloc[-1], signal_line.iloc[-1])
        
        return signal, metrics

    def _generate_signal(self, ema_fast, ema_slow, rsi, macd, macd_signal):
        """Sinyal üreticisi"""
        
        # AL sinyali: EMA yükseliş + RSI düşük + MACD pozitif
        if (ema_fast > ema_slow and 
            rsi < BUY_RSI and 
            macd > macd_signal):
            return "BUY"
        
        # SAT sinyali: EMA düşüş + RSI yüksek + MACD negatif
        elif (ema_fast < ema_slow and 
              rsi > SELL_RSI and 
              macd < macd_signal):
            return "SELL"
        
        return "HOLD"
