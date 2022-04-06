import argparse
import json
import csv
import sys
import time
from decimal import *

from settings import bitmex_accounts, gdax_accounts, coinbase_accounts, gemini_accounts, bittrex_accounts
from settings import total_deposits, manual_holding_entries, manual_btc_price
# Coinbase
from coinbase.wallet.client import Client as CB_Client

import ccxt

from kkan import CryptoPortfolio as CP
# Using an array will allow the summation of accounts across people and emails
# Potentially useful for Fund-level accounting or summing portfolio of partners


if __name__ == "__main__":

    try:

        PV = CryptoPortfolio()
        balances = PV.get_sum_balances()

    except:
        import pdb; pdb.set_trace()



