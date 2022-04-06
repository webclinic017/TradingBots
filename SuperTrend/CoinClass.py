class CoinClass:
    def __init__(self, symbol):
        ## private varibale or property in Python
        self.__coin = symbol
        if symbol == 'USDT':
            self.__pair = f'{symbol}/USD'
        else:
            self.__pair = f'{symbol}/USDT'

    ## getter method to get the properties using an object
    def get_coin(self):
        return self.__coin

    def get_pair(self):
        return self.__pair

    ## setter method to change the value 'a' using an object
    def set_coin(self, symbol):
        self.__coin = symbol
        if symbol == 'USDT':
            self.__pair = f'{symbol}/USD'
        else:
            self.__pair = f'{symbol}/USDT'

class CoinClass2:
    def __init__(self, symbol, quote):
        ## private varibale or property in Python
        self.__coin = symbol
        if symbol == 'USDT':
            self.__pair = f'{symbol}/USD'
        else:
            self.__pair = f'{symbol}/{quote}'

    ## getter method to get the properties using an object
    def get_coin(self):
        return self.__coin

    def get_pair(self):
        return self.__pair

    ## setter method to change the value 'a' using an object
    def set_coin(self, symbol, quote):
        self.__coin = symbol
        if symbol == 'USDT':
            self.__pair = f'{symbol}/USD'
        else:
            self.__pair = f'{symbol}/{quote}'

