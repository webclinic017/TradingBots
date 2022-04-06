config = {
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # PostgreSQL Database
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # PostgreSQL is used as the database to store data such as candles.
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    'databases': {
        'postgres_host': '127.0.0.1',
        'postgres_name': 'jesse_db',
        'postgres_port': 5432,
        'postgres_username': 'jesse_user',
        'postgres_password': '$Zxc5zxc5',
    },

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Caching
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # In some cases such as loading candles in the backtest mode, a
    # caching mechanism is used to make further loadings faster.
    # Valid options (so far) are: 'pickle', None
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    'caching': {
        'driver': 'pickle'
    },

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Exchanges
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # Below values are used for exchanges.
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    'exchanges': {
        # https://www.bitfinex.com
        'Bitfinex': {
            'fee': 0.002,

            # backtest mode only: accepted are 'spot' and 'futures'
            # 'spot' support is currently very limited - you can use 'futures' with leverage 1 for now
            'type': 'futures',

            # futures mode only
            'settlement_currency': 'USD',
            # accepted values are: 'cross' and 'isolated'
            'futures_leverage_mode': 'cross',
            # 1x, 2x, 10x, 50x, etc. Enter as integers
            'futures_leverage': 1,

            'assets': [
                {'asset': 'USDT', 'balance': 10_000},
                {'asset': 'USD', 'balance': 10_000},
                {'asset': 'BTC', 'balance': 0},
            ],
        },

        # https://www.binance.com
        'Binance': {
            'fee': 0.001,

            # backtest mode only: accepted are 'spot' and 'futures'
            # 'spot' support is currently very limited - you can use 'futures' with leverage 1 for now
            'type': 'spot',

            # futures mode only
            'settlement_currency': 'USDT',
            # accepted values are: 'cross' and 'isolated'
            'futures_leverage_mode': 'cross',
            # 1x, 2x, 10x, 50x, etc. Enter as integers
            'futures_leverage': 1,

            'assets': [
                {'asset': 'USDT', 'balance': 10_000},
                {'asset': 'BTC', 'balance': 1000},
            ],
        },

        # https://www.binance.com
        'Binance Futures': {
            'fee': 0.0004,

            # backtest mode only: accepted are 'spot' and 'futures'
            # 'spot' support is currently very limited - you can use 'futures' with leverage 1 for now
            'type': 'futures',

            # futures mode only
            'settlement_currency': 'USDT',
            # accepted values are: 'cross' and 'isolated'
            'futures_leverage_mode': 'cross',
            # 1x, 2x, 10x, 50x, etc. Enter as integers
            'futures_leverage': 1,

            'assets': [
                {'asset': 'USDT', 'balance': 10_000},
            ],
        },

        # https://testnet.binancefuture.com
        'Testnet Binance Futures': {
            'fee': 0.0004,

            # backtest mode only: accepted are 'spot' and 'futures'
            # 'spot' support is currently very limited - you can use 'futures' with leverage 1 for now
            'type': 'futures',

            # futures mode only
            'settlement_currency': 'USDT',
            # accepted values are: 'cross' and 'isolated'
            'futures_leverage_mode': 'cross',
            # 1x, 2x, 10x, 50x, etc. Enter as integers
            'futures_leverage': 1,

            'assets': [
                {'asset': 'USDT', 'balance': 10_000},
            ],
        },

        # https://pro.coinbase.com
        'Coinbase': {
            'fee': 0.005,

            # backtest mode only: accepted are 'spot' and 'futures'
            # 'spot' support is currently very limited - you can use 'futures' with leverage 1 for now
            'type': 'futures',

            # futures mode only
            'settlement_currency': 'USD',
            # accepted values are: 'cross' and 'isolated'
            'futures_leverage_mode': 'cross',
            # 1x, 2x, 10x, 50x, etc. Enter as integers
            'futures_leverage': 1,

            'assets': [
                {'asset': 'USDT', 'balance': 10_000},
                {'asset': 'USD', 'balance': 10_000},
                {'asset': 'BTC', 'balance': 0},
            ],
        },
    },

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Logging
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # Below configurations are used to filter out the extra logging
    # info that are displayed when the "--debug" flag is enabled.
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    'logging': {
        'order_submission': True,
        'order_cancellation': True,
        'order_execution': True,
        'position_opened': True,
        'position_increased': True,
        'position_reduced': True,
        'position_closed': True,
        'shorter_period_candles': True,
        'trading_candles': True,
        'balance_update': True,
    },

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Metrics
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # Below configurations are used to set the metrics
    # that are displayed after a backtest.
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    'metrics': {
        'sharpe_ratio': True,
        'calmar_ratio': True,
        'sortino_ratio': True,
        'omega_ratio': True,
        'winning_streak': True,
        'losing_streak': True,
        'largest_losing_trade': True,
        'largest_winning_trade': True,
        'total_winning_trades': True,
        'total_losing_trades': True,
    },

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Optimize mode
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # Below configurations are related to the optimize mode
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    'optimization': {
        # sharpe, calmar, sortino, omega
        'ratio': 'sharpe',
    },

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Data
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # Below configurations are related to the data
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    'data': {
        # The minimum number of warmup candles that is loaded before each session.
        'warmup_candles_num': 240,
    }
}

## These values are just placeholders used by Jesse at runtime
app = {
    # list of currencies to consider
    'considering_symbols': [],
    # The symbol to trade.
    'trading_symbols': [],

    # list of time frames to consider
    'considering_timeframes': ['1h', '4h'],
    # Which candle type do you intend trade on
    'trading_timeframes': ['1h'],

    # list of exchanges to consider
    'considering_exchanges': [],
    # list of exchanges to consider
    'trading_exchanges': [],

    'considering_candles': [],

    # dict of registered live trade drivers
    'live_drivers': {},

    # Accepted values are: 'backtest', 'livetrade', 'fitness'.
    'trading_mode': '',

    # variable used for test-driving the livetrade mode
    'is_test_driving': False,

    # this would enable many console.log()s in the code, which are helpful for debugging.
    'debug_mode': False,

    # this is only used for the live unit tests
    'is_unit_testing': False,
}

#backup_config = config.copy()


#def set_config(c) -> None:
#    global config
#    config['env'] = c
#    # add sandbox because it isn't in the local config file
#    config['env']['exchanges']['Sandbox'] = {
#        'type': 'spot',
#        # used only in futures trading
#        'settlement_currency': 'USDT',
#        'fee': 0,
#        'futures_leverage_mode': 'cross',
#        'futures_leverage': 1,
#        'assets': [
#            {'asset': 'USDT', 'balance': 10_000},
#            {'asset': 'BTC', 'balance': 0},
#        ],
#    }


#def reset_config() -> None:
#    global config
#    config = backup_config.copy()