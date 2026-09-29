# 🤖 Crypto Trading Bot

Binance'de otomatik alım-satım yapan, teknik analiz ile sinyal üreten, ileri seviye bir kripto para trading botu.

## 📋 Özellikler

✅ **Teknik Analiz**
- EMA (Exponential Moving Average)
- RSI (Relative Strength Index)
- Bollinger Bands
- MACD (Moving Average Convergence Divergence)

✅ **Alım/Satım Sinyalleri**
- Otomatik sinyal üretimi
- Günlük işlem limiti
- Paper trading modu

✅ **Dashboard**
- Web tabanlı gerçek zamanlı takip
- İşlem geçmişi
- Bakiye görüntüleme
- Bot durumu

✅ **Güvenlik**
- Paper trading (simülasyon) modu default
- API key şifreleme
- Rate limiting

## 🚀 Kurulum

### 1. Repoyu klonla
```bash
git clone https://github.com/duranniyazi702-stack/crypto-trading-bot.git
cd crypto-trading-bot
```

### 2. Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Bağımlılıkları kur
```bash
pip install -r requirements.txt
```

### 4. Konfigürasyonu ayarla
```bash
cp .env.example .env
```

`.env` dosyasını aç ve kendi ayarlarınızı yapın:

```env
# Binance API (opsiyonel - paper trading için gerekli değil)
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret

# Bot ayarları
TRADING_PAIR=BTC/USDT
TIMEFRAME=1h
PAPER_TRADING=True  # Paper trading aktif (simülasyon)

# Strateji parametreleri
BUY_RSI=45
SELL_RSI=70
EMA_FAST=9
EMA_SLOW=21
```

## 📍 Kullanım

### Seçenek 1: Komut Satırı Botu
```bash
python bot.py
```

Çıktı:
```
============================================================
🤖 TRADING BOT STARTED
Trading Pair: BTC/USDT
Timeframe: 1h
Interval: 60s
============================================================

============================================================
[2024-01-15 10:30:45] Analysis for BTC/USDT
============================================================
Price:        45123.45
EMA 9:        45089.23
EMA 21:       45012.34
RSI(14):      42.5
BB Upper:     45500.00
BB Middle:    45000.00
BB Lower:     44500.00
MACD:         0.000234
MACD Signal:  0.000200

>>> SIGNAL: HOLD <<<
Trades today: 0/10
============================================================
```

### Seçenek 2: Web Dashboard
```bash
python dashboard.py
```

Tarayıcıda açın: http://localhost:5000

## 🎯 Strateji Mantığı

### BUY Sinyali
- EMA Fast > EMA Slow (Yükseliş trendi)
- RSI < 45 (Aşırı satılmış)
- MACD > MACD Signal (Momentum pozitif)

### SELL Sinyali
- EMA Fast < EMA Slow (Düşüş trendi)
- RSI > 70 (Aşırı alınmış)
- MACD < MACD Signal (Momentum negatif)

## 📊 Dosya Yapısı

```
crypto-trading-bot/
├── bot.py              # Ana bot sınıfı
├── strategy.py         # Teknik analiz stratejisi
├── exchange_handler.py # Binance API işlemleri
├── dashboard.py        # Flask web dashboard
├── config.py           # Konfigürasyon
├── requirements.txt    # Python bağımlılıkları
├── .env.example        # Ortam değişkenleri örneği
├── templates/
│   └── index.html      # Web arayüzü
└── README.md           # Bu dosya
```

## ⚠️ Uyarılar

1. **Paper Trading Modu**: Bot varsayılan olarak simülasyon modunda çalışır. Gerçek para hareketleri olmaz.

2. **Gerçek Trading İçin**:
   - `.env` dosyasında `PAPER_TRADING=False` yapın
   - Binance API keylerinizi ekleyin
   - Sadece testnet ile başlayın
   - Düşük miktarlarla test edin

3. **Risk Yönetimi**:
   - Kripto para yatırımı risklidir
   - Kaybetmesi göze alınabilecek miktar ile başlayın
   - Stop-loss ve take-profit seviyelerini belirleyin
   - Bot tarafından yapılan tüm işlemleri takip edin

4. **API Güvenliği**:
   - API anahtarını hiçbir zaman paylaşmayın
   - `.env` dosyasını git'e commit etmeyin
   - IP whitelist'i kullanın

## 🔧 Gelişmiş Ayarlar

### Strateji Parametrelerini Değiştir

`config.py` dosyasında:

```python
BUY_RSI = 40       # Daha agresif alım (sayı düştükçe)
SELL_RSI = 75      # Daha agresif satım (sayı yüktikçe)
EMA_FAST = 7       # Daha hızlı tepki
EMA_SLOW = 30      # Daha yavaş trend
TRADE_SIZE_PERCENT = 0.3  # Her işlemde bakiyenin %30'u
MAX_TRADES_PER_DAY = 20   # Günde max 20 işlem
```

### Farklı Çift Ticareti

```env
TRADING_PAIR=ETH/USDT
TRADING_PAIR=XRP/USDT
TRADING_PAIR=SOL/USDT
```

### Timeframe Değiştir

```env
TIMEFRAME=15m    # 15 dakika
TIMEFRAME=4h     # 4 saat
TIMEFRAME=1d     # 1 gün
```

## 📈 Backtest

(Gelecek sürümde eklenecek)

## 🐛 Troubleshooting

### "Cannot connect to Binance"
- İnternet bağlantınızı kontrol edin
- Binance'in erişilebilir olduğunu kontrol edin
- API anahtarlarınızı kontrol edin

### "Insufficient balance"
- Paper trading'de varsayılan 1000 USDT vardır
- Gerçek trading'de hesabınızda yeterli bakiye olmalı

### "No signal generated"
- Bot 30 mum verisi bekler
- Yeterli veri gelene kadar beklemeye devam eder

## 📞 Destek

Sorunla karşılaştıysanız:
1. Issues bölümüne bakın
2. Yeni bir issue oluşturun
3. Hata mesajını tam olarak yazın

## 📄 Lisans

MIT License - Özgürce kullanabilirsiniz

## ⚡ Disclaimer

Bu bot eğitim amaçlıdır. Gerçek para ile kullanmadan önce tüm riskleri anladığınızdan emin olun. Yazarı herhangi bir kayıptan sorumlu değildir.

---

**Happy Trading! 🚀📈**
