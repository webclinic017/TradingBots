import ccxt
import config
from datetime import datetime
from datetime import timedelta
import logger
import exchanges
import CoinClass
import time
import schedule

RUNBOT_PERIOD = 60
def get_datetime():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def portfolioBalance(exchange):
    portfolio = dict()

    portfolio['exchange'] = f'{exchange}'
    portfolio['datetime'] = f'{get_datetime()}'
    gtotal = 0.0
    coinsTicker = exchanges.balances['total'] # Keyed on coin
    for coin in coinsTicker.keys():
        #binance does not have USDT as ticker
        if coin != 'USDT':
            ticker = exchanges.fetchTicker(exchange, CoinClass.CoinClass2(coin, 'USDT'))
            close = float(ticker['close'])
        else:
            close = 1.0
        qty = float(exchanges.balances['total'][coin])
        portfolio[coin] = {'totalQty' : qty, 'currentClose' : close, 'total' :  qty*close}
        gtotal += qty*close
    portfolio['grandTotal'] = gtotal
    return portfolio

def run_bot():
    exchanges.init_balances(exchanges.binance)
    portfolio = portfolioBalance(exchanges.binance)
    print(logger.formatMsg(portfolio, json=True))
    logger.appendTo('portfolio', portfolio)

print(f'RUNBOT_PERIOD={RUNBOT_PERIOD} minutes.')
run_bot()
schedule.every(RUNBOT_PERIOD).minutes.do(run_bot)
while True:
    schedule.run_pending()
    time.sleep(1)
