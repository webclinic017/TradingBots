# https://github.com/hackingthemarkets/supertrend-crypto-bot

import ccxt
import config
import schedule
import pandas as pd
import warnings
import numpy as np
from datetime import datetime
from datetime import timedelta
import time
import sys
import logger
import csv

logger.init('stbRun')

# Will fetch LIMIT price actions and dump to .CSV file.
# Will not attempt limit orders
INDEVELOPMENT = False

# extra params and overrides if needed
buysell_params = {
    'test': INDEVELOPMENT,  # test order if it's valid, but don't actually place it
}

RUNBOT_PERIOD = 60 #seconds
TIMEFRAME = '15m'
LIMIT = 100
BUYSELL_QTY = 1000
MAXBUYSELL_QTY = 2000.0

#in_position = True

balances = dict()

warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': config.BINANCE_API_KEY,
    'secret': config.BINANCE_SECRET_KEY,
    'timeout': 50000,
    'enableRateLimit': True,
})

class CoinClass:
    def __init__(self, coin):
        ## private varibale or property in Python
        self.__coin = coin
        self.__pair = f'{coin}/USDT'

    ## getter method to get the properties using an object
    def get_coin(self):
        return self.__coin

    def get_pair(self):
        return self.__pair

    ## setter method to change the value 'a' using an object
    def set_coin(self, coin):
        self.__coin = coin
        self.__pair = f'{coin}/USDT'

class CoinClass2:
    def __init__(self, symbol, quote):
        ## private varibale or property in Python
        self.__coin = symbol, quote
        self.__pair = f'{symbol}/{quote}'

    ## getter method to get the properties using an object
    def get_coin(self):
        return self.__coin

    def get_pair(self):
        return self.__pair

    ## setter method to change the value 'a' using an object
    def set_coin(self, symbol, quote):
        self.__coin = symbol
        self.__pair = f'{symbol}/{quote}'


# Binance error: "Timestamp for this request was 1000ms ahead of the server's time."
# C:\> net stop w32time
# C:\> w32tm /unregister
# C:\> w32tm /register
# C:\> net start w32time
# C:\> w32tm /resync
def binanceCheckServerTime():
    b = ccxt.binance()
    logger.write(b.milliseconds(), b.nonce(), time.time()*1000, time.time()*1000 - float(b.public_get_time()['serverTime']))
    logger.write(b.milliseconds(), b.nonce(), time.time()*1000, time.time()*1000 - float(b.public_get_time()['serverTime']))
    logger.write(b.milliseconds(), b.nonce(), time.time()*1000, time.time()*1000 - float(b.public_get_time()['serverTime']))
    logger.write(b.milliseconds(), b.nonce(), time.time()*1000, time.time()*1000 - float(b.public_get_time()['serverTime']))

def get_datetime_str():
    return str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))


# periods = input(title="ATR Period", type=input.integer, defval=10)
# src = input(hl2, title="Source") #hl2 = (high + low) / 2
# multiplier = input(title="ATR Multiplier", type=input.float, step=0.1, defval=3.0)
# UseSMA = input(title="Change ATR Calculation Method ?", type=input.bool, defval=true)
# 
# # tr = max(high - low, abs(high - close[1]), abs(low - close[1]))
# atr = useSMA ? sma(tr, periods) : atr(periods) 
# lowB = src - (multiplier * atr)
# lowB1 = nz(lowB[1], lowB)
# lowB := close[1] > lowB1 ? max(lowB, lowB1) : lowB

# upB = src + (multiplier * atr)
# upB1 = nz(upB[1], upB)
# upB := close[1] < upB1 ? min(upB, upB1) : upB
# trend = nz(trend[1], 1)
# trend := trend == -1 and close > upB1 ? 1 : trend == 1 and close < lowB1 ? -1 : trend
# buySignal = trend == 1 and trend[1] == -1
# sellSignal = trend == -1 and trend[1] == 1

# TradingView: tr = max(high - low, abs(high - close[1]), abs(low - close[1]))
# close[1] being previous close
def tr(data):
    data['high-low'] = abs(data['high'] - data['low'])

    data['previous_close'] = data['close'].shift(1)
    data['high-pc'] = abs(data['high'] - data['previous_close'])
    data['low-pc'] = abs(data['low'] - data['previous_close'])
    
    tr = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)
    return tr

def atr(df, period):
    df['tr'] = tr(df)
    atr = df['tr'].rolling(period).mean()
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

    #Force uptrend!
    #df['in_uptrend'][97] = False                 
    #df['in_uptrend'][98] = True                 

    #Force downtrend
    #df['in_uptrend'][97] = True
    #df['in_uptrend'][98] = False
    
    return df

def supertrend(bars, coin : CoinClass):
    #Exclude the last row (:-1) as it is currently live and changing
    pair = coin.get_pair()
    df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.insert(0, 'symbol', pair)
    return supertrend_df(df)

def check_buy_sell_signals(df, coin : CoinClass):
    #global in_position
    logger.write('Checking for NEW buy/uptrend OR NEW sell/downtrend signals...')
    #logger.write(f'In position = {in_position}')
    logger.write(df.tail(2))
    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1
    pair = coin.get_pair()

    symbol = coin.get_coin()
    totQtyBalance = get_balanceCoin(symbol)

    if not df['in_uptrend'][previous_row_index] and df['in_uptrend'][last_row_index]:
        logger.write(f'New uptrend detected! Market BUY \'{pair}\' \'{BUYSELL_QTY}\' @ {df["close"][last_row_index]}$:')
        if totQtyBalance < MAXBUYSELL_QTY:
            try:
                if INDEVELOPMENT:
                    buy_order = f'exchange.create_market_buy_order({pair}, {BUYSELL_QTY})' #, buysell_params)'
                else:
                    buy_order = exchange.create_market_buy_order(pair, BUYSELL_QTY) #, params)
                logger.write(f'Buy order: {buy_order}')
                #in_position = True
            except:
                type, value, traceback = sys.exc_info()
                logger.write(f'create_market_buy_order() exception: {str(type)} {str(value)}')
        else:
            logger.write(f'Already MAXED qty totQtyBalance={totQtyBalance} > MAXBUYSELL_QTY={MAXBUYSELL_QTY}. Waiting for sell trend. :)')
    
    if df['in_uptrend'][previous_row_index] and not df['in_uptrend'][last_row_index]:
        logger.write(f'Downtrend detected! Market SELL \'{pair}\' \'{BUYSELL_QTY}\' @ {df["close"][last_row_index]}$:')
        if totQtyBalance > 0.0:
            try:
                isPriceGoodForProfit, price, currentPrice = priceGoodForProfit(df, last_row_index, coin)
                if isPriceGoodForProfit:
                    if INDEVELOPMENT:
                        sell_order = f'exchange.create_market_sell_order({pair}, {BUYSELL_QTY})' #, buysell_params)'
                    else:
                        bs_qty = min(totQtyBalance, BUYSELL_QTY)
                        sell_order = exchange.create_market_sell_order(pair, bs_qty) #, buysell_params)
                    logger.write(f'Sell order: {sell_order}')
                    #in_position = False
                else:
                    logger.write(f'Sell order skipped: minPrice to cover={price} CurrentPrice={currentPrice}')
            except:
                type, value, traceback = sys.exc_info()
                logger.write(f'create_market_sell_order() exception: {type} {value}')
        else:
            logger.write(f'No more to sell totQtyBalance={totQtyBalance}. Waiting for buy trend. :)')

    if (df['in_uptrend'][previous_row_index] and df['in_uptrend'][last_row_index]) or (not df['in_uptrend'][previous_row_index] and not df['in_uptrend'][last_row_index]):
        logger.write('No change in trend detected!')

def fetch_ohlcv(coin : CoinClass):
    logger.write('----------')
    pair = coin.get_pair()
    logger.write(f'Fetching \'{pair}\' \'{LIMIT}\' x \'{TIMEFRAME}\' bars before {get_datetime_str()}')
    try:
        bars = exchange.fetch_ohlcv(pair, timeframe=TIMEFRAME, limit=LIMIT)
    except:
        type, value, traceback = sys.exc_info()
        logger.write(f'fetch_ohlcv() exception: {type} {value}')
    return bars

def run_bot_dev(coin : CoinClass):
    try:
        bars = fetch_ohlcv(coin)
        supertrend_data = supertrend(bars, coin)
        logger.write(supertrend_data.info())  
    
        logger.write(supertrend_data.head(5))
        for r in range (0, 3):
            try:
                logger.write(f'r={r}')
                logger.write(supertrend_data['timestamp'][r])
            except:
                type, value, traceback = sys.exc_info()
                logger.write(f'run_bot_dev() exception: {value} {type}')

        logger.write(f'index={len(supertrend_data.index)}')
        logger.write(supertrend_data.tail(5))

        for x in range (97, 101):
            try:
                logger.write(f'x={x}')
                logger.write(supertrend_data['timestamp'][x])
            except:
                type, value, traceback = sys.exc_info()
                logger.write(f'run_bot_dev() exception: {type} {value}')

        #logger.write(supertrend_data['timestamp':previous_row_index])
        #logger.write(supertrend_data['timestamp'][last_row_index])
        #logger.write(supertrend_data['timestamp'][len(supertrend_data.index)])

        #supertrend_data.to_csv('output-binance-15m.csv')

        isPriceGoodForProfit, price, currentPrice = priceGoodForProfit(supertrend_data, coin)
        logger.write(f'isPriceGoodForProfit={isPriceGoodForProfit} price={price} currentPrice={currentPrice}')

    except:
        pass

def run_bot():
    global balances
    try:
        balances = get_balances()
        #trades = get_MyTrades()

        #for each coin
        symbol = 'ZIL'
        coin = CoinClass(symbol)

        bars = fetch_ohlcv(coin)
        supertrend_data = supertrend(bars, coin)
        check_buy_sell_signals(supertrend_data, coin)
    except:
        type, value, traceback = sys.exc_info()
        logger.write(f'run_bot() exception: {type} {value}')

# If Balance is 0.0, it will be absent from dict balances
def get_balanceCoin(symbol):
    global balances
    try:
        return balances[symbol]['total']
    except:
        return 0.0

def get_balances():
    bals = exchange.fetchBalance()
    #logger.write(type(balances))
    bals_nonempty = dict()
    bals_nonempty['exchange'] = exchange
    bals_nonempty['updateTime'] = bals['info']['updateTime']
    bals_nonempty['accountType'] = bals['info']['accountType']
    bals_nonempty['balances'] = list()

    balance_assets = bals['info']['balances']
    #logger.write(type(bal_assets), balance_assets)
    for item in balance_assets:
        if not(float(item['free']) == 0.0 and float(item['locked']) == 0.0):
            bals_nonempty['balances'].append(item)

    balance_totals = bals['total'] # Keyed on coin
    for coin in balance_totals.keys():
        if balance_totals[coin] != 0:
            bals_nonempty[coin] = bals[coin]
    
    if INDEVELOPMENT:
        logger.write(f'bals={bals_nonempty}')
    return bals_nonempty

def priceGoodForProfit(df, last_row_index, coin : CoinClass):
    price = goodPriceToSell(coin)
    return df['close'][last_row_index] > price, price, df['close'][last_row_index]

def goodPriceToSell(coin : CoinClass):
    global balances
    symbol = coin.get_coin()
    coinTotQtyBalance = get_balanceCoin(symbol)
    
    trades = get_MyTrades(coin)
    result = get_MyTradesMaxBuyPrice(trades, coinTotQtyBalance)

    if INDEVELOPMENT:
        logger.write(f'{symbol} coinTotQtyBalance={coinTotQtyBalance}')
        logger.write(f'result={result}')

    #todo: should we add a min. % profit to this maxbuyprice?
    return result

def get_MyTradesMaxBuyPrice(trades, balanceTotQtyToCover):
    qty = 0.0
    priceToCoverLoss = 0.0
    tradeToCoverLoss = {}
    lastTradeToCoverQty = {}
    for t in reversed(trades):
        if t['side'] == 'buy':
            qty = qty + float(t['amount'])
            if qty <= balanceTotQtyToCover:
                lastTradeToCoverQty = t
                tprice = float(t['price'])
                if tprice > priceToCoverLoss:
                    tradeToCoverLoss = t
                    priceToCoverLoss = tprice
            else:
                logger.write(f'priceToCoverLoss={priceToCoverLoss}')
                logger.write(f'tradeToCoverLoss={tradeToCoverLoss}')
                logger.write(f'lastTradeToCoverQty={lastTradeToCoverQty}')
                return priceToCoverLoss
            
def get_MyTrades(coin : CoinClass):
    monthAgo = datetime.utcnow() - timedelta(days=10)
    monthAgoMs = int(time.mktime(monthAgo.timetuple()))
    #logger.write(f'OneMonthAgo={monthAgoMs}ms')
    trades = exchange.fetchMyTrades(symbol = coin.get_pair(), since = monthAgoMs)
    #logger.write(trades)
    return trades

def get_MyTrades2(coin : CoinClass2):
    monthAgo = datetime.utcnow() - timedelta(days=10)
    monthAgoMs = int(time.mktime(monthAgo.timetuple()))
    #logger.write(f'OneMonthAgo={monthAgoMs}ms')
    trades = exchange.fetchMyTrades(symbol = coin.get_pair(), since = monthAgoMs)
    logger.write(trades)
    return trades

def get_Orders(coin : CoinClass):
    orders = exchange.fetchOrders(symbol = coin.get_pair())
    logger.write(orders)

def get_OpenOrders(coin : CoinClass):
    openOrders = exchange.fetchOpenOrders(symbol = coin.get_pair())
    logger.write(openOrders)

# csv.DictReader class provides an iterable interface over the csv data source where items are dictionaries:
def load_CoinsToTrade():
    #input_file = csv.reader(open("coinstotrade.csv", "r"), delimiter=',')
    input_file = csv.DictReader(open("coins.csv", "r"), delimiter=',')
    #for row in input_file:
    #    print(row)
    return input_file

# MAIN =====
logger.write('START ==========')
logger.write(f'Exchange name={exchange} v={exchange.version} has={exchange.has}')

try:
    if INDEVELOPMENT:
        
        coinsToTrade = load_CoinsToTrade()
        for coin in coinsToTrade:
            coinToTrade = CoinClass2(coin['SYMBOL'], coin['QUOTE'])
            print(coinToTrade.get_pair())
            trades = get_MyTrades2(coinToTrade)

        #balances = get_balances()
        #logger.write(balances)
        # trades = get_MyTrades()

        #for each coin
        #symbol = 'ZIL'
        #coin = CoinClass(symbol)

        #logger.write(goodPriceToSell(coin))

        #logger.write(get_MyTradesMinPrice(get_MyTrades('UNI/USDT')))
        #get_MyTrades('ZIL/USDT')
        #get_Orders('ZIL/USDT')
        #get_OpenOrders('ZIL/USDT')
        #get_balance()

        #run_bot_dev(coin)

    else:
        run_bot()

        schedule.every(RUNBOT_PERIOD).seconds.do(run_bot)
        while True:
            schedule.run_pending()
            time.sleep(1)
except:
    type, value, traceback = sys.exc_info()
    logger.write(f'Main exception: {type} {value}')
finally:
    logger.logFile.close()