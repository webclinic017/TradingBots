import ccxt
import config
import CoinClass
import json as _json
import sys

exchange_class = getattr(ccxt, 'binance')
binance = exchange_class({
    'apiKey': config.BINANCE_API_KEY,
    'secret': config.BINANCE_SECRET_KEY,
    'timeout': 50000,
    'enableRateLimit': True,
})

#exchange_class = getattr(ccxt, 'kraken')
#kraken = exchange_class({
#    'apiKey': config.KRAKEN_API_KEY,
#    'secret': config.KRAKEN_SECRET_KEY,
#    'timeout': 50000,
#    'enableRateLimit': True,
#})

#exchange_class = getattr(ccxt, 'ftx')
#ftx = exchange_class({
#    'apiKey': config.FTX_API_KEY,
#    'secret': config.FTX_API_SECRET,
#    'timeout': 50000,
#    'enableRateLimit': True,
#})

balances = dict()

# Binance error: "Timestamp for this request was 1000ms ahead of the server's time."
# C:\> net stop w32time
# C:\> w32tm /unregister
# C:\> w32tm /register
# C:\> net start w32time
# C:\> w32tm /resync
def binanceCheckServerTime():
    b = ccxt.binance()
    logger.write(b.milliseconds(), b.noce(), time.time()*1000, time.time()*1000 - float(b.public_get_time()['serverTime']))
    logger.write(b.milliseconds(), b.nonce(), time.time()*1000, time.time()*1000 - float(b.public_get_time()['serverTime']))
    logger.write(b.milliseconds(), b.nonce(), time.time()*1000, time.time()*1000 - float(b.public_get_time()['serverTime']))
    logger.write(b.milliseconds(), b.nonce(), time.time()*1000, time.time()*1000 - float(b.public_get_time()['serverTime']))

# If Balance is 0.0, it will be absent from dict balances
# get_balances must be called before to init balances dict
def get_balanceCoin(symbol):
    global balances
    try:
        return balances[symbol]['total']
    except:
        return 0.0

def init_balances(exchange):
    bals = exchange.fetchBalance()
    #logger.write('get_balances ----------')
    #logger.write(exchange)
    #logger.write(bals)

    #print(_json.dumps(bals))

    balances['exchange'] = f'{exchange}'
    if exchange == 'Binance':
        balances['updateTime'] = bals['info']['updateTime']
    elif exchange == 'Kraken':
        balances['updateTime'] = ''
    elif exchange == 'Ftx':
        balances['updateTime'] = ''

    #bals_nonempty['accountType'] = bals['info']['accountType']
    balances['balances'] = list()

    balance_assets = bals['info']['balances']
    #logger.write(type(bal_assets), balance_assets)
    for item in balance_assets:
        if not(float(item['free']) == 0.0 and float(item['locked']) == 0.0):
            balances['balances'].append(item)

    balance_totals = bals['total'] # Keyed on coin
    balances['total'] = dict()
    for coin in balance_totals.keys():
        if balance_totals[coin] != 0:
            balances[coin] = bals[coin]
            balances['total'].update({ coin : bals['total'][coin] })
    
    #if INDEVELOPMENT:
    #    logger.write(f'bals indev={bals_nonempty}')
    #print(type(balances))
    #print(balances)
    #print(_json.dumps(balances))

def fetchTicker(exchange, coin : CoinClass.CoinClass2):
    if (exchange.has['fetchTickers']):
        return exchange.fetch_ticker(coin.get_pair()) # listed ticker