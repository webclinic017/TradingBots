# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Make sure to read the docs about routes if you haven't already:
# https://docs.jesse.trade/docs/routes.html
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from jesse.utils import anchor_timeframe

# trading routes
routes = [
    #('Binance', 'BTC-USDT', '1h', 'SMACrossover'),
    ('Binance', 'BTC-USDT', '1h', 'donchian'),
]

# in case your strategy requires extra candles, timeframes, ...
extra_candles = [
    ('Binance', 'BTC-USDT', anchor_timeframe('1h')),
]
