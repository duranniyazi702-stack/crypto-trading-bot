from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import threading
import json
from datetime import datetime
from bot import TradingBot
from config import FLASK_PORT, TRADING_PAIR

app = Flask(__name__)
CORS(app)

bot_instance = None
bot_thread = None

def start_bot_thread():
    """Botu ayrı thread'te çalıştır"""
    global bot_thread, bot_instance
    if bot_instance and not bot_instance.running:
        bot_thread = threading.Thread(target=bot_instance.run, kwargs={"interval": 60})
        bot_thread.daemon = True
        bot_thread.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def get_status():
    """Bot durumu"""
    if not bot_instance:
        return jsonify({"status": "not_initialized", "error": "Bot not initialized"})
    
    return jsonify({
        "status": "running" if bot_instance.running else "stopped",
        "trading_pair": TRADING_PAIR,
        "trades_today": bot_instance.trades_today,
        "total_trades": len(bot_instance.trade_history),
        "usdt_balance": bot_instance.exchange.get_balance("USDT"),
        "coin_balance": bot_instance.exchange.get_position(TRADING_PAIR)
    })

@app.route("/api/trades")
def get_trades():
    """İşlem geçmişi"""
    if not bot_instance:
        return jsonify({"trades": []})
    
    trades = []
    for trade in bot_instance.trade_history:
        trades.append({
            "timestamp": trade["timestamp"].isoformat(),
            "side": trade["side"],
            "amount": trade["amount"],
            "price": trade["price"],
            "metrics": trade["metrics"]
        })
    
    return jsonify({"trades": trades})

@app.route("/api/start", methods=["POST"])
def start_bot():
    """Botu başlat"""
    global bot_instance
    try:
        if not bot_instance:
            bot_instance = TradingBot()
        
        if not bot_instance.running:
            start_bot_thread()
            return jsonify({"status": "success", "message": "Bot started"})
        else:
            return jsonify({"status": "info", "message": "Bot already running"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/api/stop", methods=["POST"])
def stop_bot():
    """Botu durdur"""
    global bot_instance
    if bot_instance:
        bot_instance.stop()
        return jsonify({"status": "success", "message": "Bot stopped"})
    return jsonify({"status": "info", "message": "Bot not running"})

@app.route("/api/config")
def get_config():
    """Konfigürasyonu al"""
    from config import BUY_RSI, SELL_RSI, EMA_FAST, EMA_SLOW, PAPER_TRADING
    return jsonify({
        "buy_rsi": BUY_RSI,
        "sell_rsi": SELL_RSI,
        "ema_fast": EMA_FAST,
        "ema_slow": EMA_SLOW,
        "paper_trading": PAPER_TRADING
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=False)
