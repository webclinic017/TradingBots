# python-binance
# TA-Lib  https://github.com/mrjbq7/ta-lib
# numpy
# websocket_client

import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *

#TRADE_SYMBOL = 'ETHUSD'
#SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

#TRADE_SYMBOL = 'ADAUSDT'
#SOCKET = "wss://stream.binance.com:9443/ws/adausdt@kline_1m"

TRADE_SYMBOL = 'DOTUSDT'
SOCKET = "wss://stream.binance.com:9443/ws/dotusdt@kline_1m"

TRADE_SYMBOL = 'DOTUSDT'
SOCKET = "wss://stream.binance.com:9443/ws/dotusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 65
RSI_OVERSOLD = 35
TRADE_QUANTITY = 0.05

closes = []
in_position = False

client = Client(config.API_KEY, config.API_SECRET, tld='us')

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("Sending order: client.create_order(symbol=" + str(symbol) + ", side=" + str(side) + ", type=" + order_type + ", quantity=" + str(quantity) + ")")
        
        #print("sending order")
        #order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        #print(order)
    except Exception as e:
        print("Exception occured - {}".format(e))
        return False

    return True

    
def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes, in_position
    
    #print('received message')
    json_message = json.loads(message)
    print(message)
    #pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("Candle closed at {}.".format(close))
        closes.append(float(close))
        print("closes", closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("All RSIs calculated so far:", rsi)
            last_rsi = rsi[-1]
            print("Current rsi is {}.".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought! Sell! Sell! Sell!")
                    # put binance sell logic here
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = False
                else:
                    print("Overbought! But we don't own any. Order skipped.")
            
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("Oversold! But you already own it. Order skipped.")
                else:
                    print("Oversold! Buy! Buy! Buy!")
                    # put binance buy order logic here
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = True

         
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
