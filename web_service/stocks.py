from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import database
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

model = None

def fetch_ohlcv(symbol):
    end_time = datetime.now()

    start_time = end_time - timedelta(days=120)

    time_start = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    time_end = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    url = f"https://rest.coinapi.io/v1/ohlcv/BINANCE_SPOT_{symbol}_USDT/history?period_id=1DAY&time_start={time_start}&time_end={time_end}"
    
    headers = { "X-CoinAPI-Key": "CF4FE12E-B84A-4CE3-8152-7E8229F234D6" }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        if response.content:
            data = response.json()
        else:
            print("Response is empty.")
            return None
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None
    
    return data
    
def load_stock_data(stock_symbol):
    
    data = fetch_ohlcv(stock_symbol)
    df = pd.DataFrame(data)
    df = df[['time_period_start', 'price_close', 'volume_traded']]
    df.rename(columns={'time_period_start': 'Date', 'price_close': 'Close', 'volume_traded': 'Volume'}, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df['10MA'] = df['Close'].rolling(window=10).mean()
    df['50MA'] = df['Close'].rolling(window=50).mean()

    def cal_RSI(data, window=14):
        delta = data['Close'].diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()

        rs = avg_gain / avg_loss
        RSI = 100 - (100 / (1 + rs))

        return RSI

    df['RSI'] = cal_RSI(df)

    return df

def train_model(stock_symbol):
    global model
    data = load_stock_data(stock_symbol)
    print("Data loaded:", data.shape)
    train_size = int(len(data) * 0.8)  
    test_data = data[train_size:]
    train_data = data[:train_size]
    print("Training data:", train_data.shape)

    model = RandomForestRegressor(n_estimators=100, random_state=42) 

    
    train_data = train_data.copy()
    test_data = test_data.copy()

    train_data.dropna(inplace=True)
    test_data.dropna(inplace=True)
    

    X_train = train_data[['10MA', '50MA', 'RSI']]
    y_train = train_data['Close']
    model.fit(X_train, y_train)

def insert_stock_prediction(connection, Symbol, CurrentPrice, Prediction, Decision, PredictionDate):
    try:
        cursor = connection.cursor()

        insert_query = "INSERT INTO stock_predictions (symbol, CurrentPrice, Prediction, decision, PredictionDate) VALUES (%s, %s, %s, %s, %s)"
        
        cursor.execute(insert_query, (Symbol, CurrentPrice, Prediction, Decision, PredictionDate))
        connection.commit()

        print("Data inserted successfully")

    except Exception as e:
        print(f"Error inserting data into the database: {e}")

def fetch_latest_price(symbol):
    # Set the period to 1DAY and fetch only the latest data
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)
    url = f"https://rest.coinapi.io/v1/ohlcv/BINANCE_SPOT_{symbol}_USDT/latest?period_id=1DAY"
    headers = {"X-CoinAPI-Key": "CF4FE12E-B84A-4CE3-8152-7E8229F234D6"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data:
            # Assuming the latest data point is the first in the list
            latest_data = data[0]
            return latest_data['price_close']
        else:
            print("No data available.")
            return None
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_symbol = request.form['coin']
        try:
            train_model(stock_symbol)
        except Exception as e:
            print("Error at index 1")
            return render_template('index.html', error=str(e))

        return render_template('prediction.html', symbol=stock_symbol)
    else:
        print("Error at index 2")
        return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_stock_price():
    try:
        stock_symbol = request.form['coin']

        train_model(stock_symbol)

        stock_data = load_stock_data(stock_symbol)

        latest_data = stock_data.iloc[-1]

        input_data = {
            '10MA': latest_data['10MA'],
            '50MA': latest_data['50MA'],
            'RSI': latest_data['RSI']
        }
        input_df = pd.DataFrame([input_data])

        predictions = model.predict(input_df)

        if predictions[0] > stock_data['Close'].iloc[-1]:
            signal = 'BUY'
        else:
            signal = 'SELL'

        current_price = fetch_latest_price(stock_symbol)
        
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        connection = database.connect_to_database()
        if connection:
            insert_stock_prediction(connection, stock_symbol,current_price, predictions[0], signal, date)
            connection.close()

        response = {
            'predictions': predictions.tolist(),
            'signal': signal,
            'symbol': stock_symbol,
            'current_price': current_price
        }

        return render_template('prediction.html', result=response)

    except Exception as e:
        print(f"Error at predict_stock_price: {e}")
        return render_template('error.html', error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
