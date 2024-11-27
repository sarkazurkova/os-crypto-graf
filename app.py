from flask import Flask, render_template, request
import yfinance as yf
from datetime import datetime, timedelta

app = Flask(__name__)

# Funkce pro získání dat kryptoměny
def get_crypto_data(crypto_symbol, period):
    crypto = yf.Ticker(crypto_symbol)

    # Pokud je požadováno období "1 den", použijeme hodinová data
    if period == "1d":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
        data = crypto.history(start=start_date, end=end_date, interval="1h")  # Interval 1 hodina
    else:
        data = crypto.history(period=period)  # Standardní data podle zadaného období

    return data

@app.route('/', methods=['GET'])
def index():
    crypto_symbol = request.args.get('crypto_symbol', 'BTC-USD')  # Výchozí kryptoměna
    period = request.args.get('period', '1y')  # Výchozí období (1 rok)

    # Získání dat
    data = get_crypto_data(crypto_symbol, period)
    dates = data.index.strftime('%Y-%m-%d %H:%M' if period == "1d" else '%Y-%m-%d').tolist()
    prices = data['Close'].tolist()

    return render_template(
        'index.html',
        crypto_symbol=crypto_symbol,
        period=period,
        dates=dates,
        prices=prices
    )

if __name__ == '__main__':
    app.run(debug=True)
