# https://github.com/hackingthemarkets/supertrend-crypto-bot

import ccxt
import configPST as config
import schedule
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

import warnings
warnings.filterwarnings('ignore')

import numpy as np

from datetime import datetime
import time
import csv
import json
import sys

# Will fetch LIMIT price actions and dump to .CSV file.
# Will not attempt limit orders
INDEVELOPMENT = False

exchange = ccxt.ftx({
    "apiKey": config.FTX_API_KEY,
    "secret": config.FTX_API_SECRET
})

# FTX does not have a sandbox API/URL
#exchange.set_sandbox_mode(INDEVELOPMENT)

# extra params and overrides if needed
params = {
    'test': INDEVELOPMENT,  # test order if it's valid, but don't actually place it
}

TIMEFRAME='15m'
LIMIT=10

SYMBOL = 'SRM/USDT'  

#def toCsv(df):
#    with open('output.csv', 'w') as csvfile:
#        csvwriter = csv.writer(csvfile)
#        for row in df.items():
#            csvwriter.writerow(row)

def tr(data):
    data['previous_close'] = data['close'].shift(1)
    data['high-low'] = abs(data['high'] - data['low'])
    data['high-pc'] = abs(data['high'] - data['previous_close'])
    data['low-pc'] = abs(data['low'] - data['previous_close'])

    tr = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)

    return tr

def atr(data, period):
    data['tr'] = tr(data)
    atr = data['tr'].rolling(period).mean()

    return atr

def supertrend_df(df, period=7, atr_multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    df['atr'] = atr(df, period)
    df['upperband'] = hl2 + (atr_multiplier * df['atr'])
    df['lowerband'] = hl2 - (atr_multiplier * df['atr'])
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current - 1

        if df['close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True
        elif df['close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False
        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]

            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]

    return df


in_position = False

def check_buy_sell_signals(df):
    global in_position

    print("Checking for buy and sell signals...")
    print(df.tail(5))
    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1

    if not df['in_uptrend'][previous_row_index] and df['in_uptrend'][last_row_index]:
        print("Changed to uptrend, buy:")
        if not in_position:
            order = exchange.create_market_buy_order(SYMBOL, 30, params)
            print(order)
            in_position = True
        else:
            print("Already in position, nothing to do.")
    
    if df['in_uptrend'][previous_row_index] and not df['in_uptrend'][last_row_index]:
        if in_position:
            print("Changed to downtrend, sell:")
            order = exchange.create_market_sell_order(SYMBOL, 30, params)
            print(order)
            in_position = False
        else:
            print("You aren't in position, nothing to sell.")

def supertrend(bars):
    df = pd.DataFrame(bars[:], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.insert(0, 'symbol', SYMBOL)

    return supertrend_df(df)

def fetch_ohlcv():
    print("----------")
    print(f"Fetching '" + str(SYMBOL) + "' '" + str(LIMIT) + "' '" + str(TIMEFRAME) + "' bars before " + str(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
    bars = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=LIMIT)
    return bars

def run_bot_dev():
    bars = fetch_ohlcv()
    supertrend_data = supertrend(bars)
    #print(supertrend_data.info())        
    supertrend_data.to_csv('output-ftx-15m.csv')
    
def run_bot():
    bars = fetch_ohlcv()
    supertrend_data = supertrend(bars)
    #print(supertrend_data.info())        
    
    check_buy_sell_signals(supertrend_data)

# ------- MAIN
print("Exchange info:")
print(exchange, exchange.version, exchange.has)
#print(json.dumps(exchange, sort_keys=True, indent=2))

try:
    order = exchange.create_market_buy_order(SYMBOL, 30, params)
    print(order)
    in_position = True
except:
    type, value, traceback = sys.exc_info()
    print('Error type: %s Create order exception: %s' % (type, value))

#order = exchange.create_market_sell_order(SYMBOL, 30, params)
#print(order)
#in_position = False

if INDEVELOPMENT:
    run_bot_dev()
else:
    schedule.every(10).seconds.do(run_bot)

    while True:
        schedule.run_pending()
        time.sleep(1)
