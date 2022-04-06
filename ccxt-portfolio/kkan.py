
import argparse
import json
import csv
import sys
import time
from decimal import *
import datetime

from settings import binance_accounts, bitmex_accounts, gdax_accounts, coinbase_accounts, gemini_accounts, bittrex_accounts
#from settings import cryptopia_accounts
from settings import total_deposits, manual_holding_entries # , manual_btc_price
# Coinbase
from coinbase.wallet.client import Client as CB_Client

import ccxt
## Originally built with  ccxt (1.10.337)

# Using an array will allow the summation of accounts across people and emails
# Potentially useful for Fund-level accounting or summing portfolio of partners

class CryptoPortfolio:
    def __init__(self):
        self.output =  open('kkan_log.txt','a+')

        # Preload holdings not reflected in API Key portfolios. (coins in transit, hard wallet, etc.)
        self.portfolio_info = manual_holding_entries

        #
        self.bitmex     = None # Using multiple accounts will leave the last Conn assigned here
        self.bittrex    = None
        self.default_bittrex = ccxt.bittrex()
        self.cb_client  = None
        self.cryptopia  = None
        self.gdax       = None
        self.gemini     = None
        self.cryptopia  = None

        self.bitmex_margin_stake = Decimal(0)

        # exchanges = {
        #     'binance': self.load_binance_accounts,
        #     'bitmex' :

        # }

        self.load_binance_accounts();
        # except Exception, e: self.banner("Binance error: "+str(e) )
        try: self.load_bitmex_accounts()
        except: self.banner("Bitmex error: "+str(e) )
        try: self.load_coinbase_accounts()
        except: self.banner("Coinbase error: "+str(e) )
        try: self.load_cryptopia_accounts()
        except: self.banner("Cryptopia error: "+str(e) )
        try: self.load_gdax_accounts()
        except: self.banner("GDAX error: "+str(e) )
        try: self.load_gemini_accounts()
        except: self.banner("Gemini error: "+str(e) )
        try: self.load_bittrex_accounts()
        except: self.banner("Bittrex error: "+str(e) )

    @staticmethod
    def banner(str):
        print( "*" * 25)
        print("*  "+str+ "   ** ")
        print("*" * 25)

    def insert_portfolio_object(self, exchange, obj):
        # Initiate Portfolio Info object
        if exchange not in self.portfolio_info:
            self.portfolio_info[exchange] = []

        if type(obj) == list: # ["GDAX", "Coinbase", "Gemini"]
            self.portfolio_info[exchange] += obj # Add {}s from []
        elif type(obj)==dict:
            self.portfolio_info[exchange].append( obj ) # Insert {} to []
        else:
            raise Exception("Invalid portfolio/account object passed to insert_portfolio_object")

    # Load Bitmex Account
    def load_bitmex_accounts(self):
        for account_email, config in bitmex_accounts.iteritems():
            self.bitmex     = ccxt.bitmex({'apiKey':config['API_KEY'], 'secret':config['API_SECRET']})
            # BitmexConnection = bitmex.BitMEX(base_url=BITMEX_API_BASE, apiKey=config['API_KEY'], apiSecret=config['API_SECRET'])
            # account_data = BitmexConnection.get_account_info() # returns {}

            balance = self.bitmex.fetchBalance()
            # Use all info here, want to see what is open on margins
            summary = {'BTC': balance['BTC'] }

            self.insert_portfolio_object('Bitmex', summary)
            # print json.dumps(balance,  indent=2)

    def load_binance_accounts(self):
        for account_email, config in binance_accounts.iteritems():
            self.binance    = ccxt.binance({'verbose': False, 'apiKey':config['API_KEY'], 'secret':config['API_SECRET']})
            # USDT will show up in this balance, but not in B wallets UI in bittrex
            balances = self.binance.fetchBalance()
            balance_totals = balances['total'] # Keyed on coin
            for coin in balance_totals.keys():
                if balance_totals[coin] == 0:
                    del balance_totals[coin]

            self.insert_portfolio_object('Binance', balance_totals)

    # def load_bittrex_accounts(self):
    #     self.bittrex    = ccxt.bittrex()
    def load_bittrex_accounts(self):
        for account_email, config in bittrex_accounts.iteritems():
            self.bittrex    = ccxt.bittrex({'verbose': False, 'apiKey':config['API_KEY'], 'secret':config['API_SECRET']})
            # USDT will show up in this balance, but not in B wallets UI in bittrex
            balances = self.bittrex.fetchBalance()
            balance_totals = balances['total'] # Keyed on coin
            for coin in balance_totals.keys():
                if balance_totals[coin] == 0:
                    del balance_totals[coin]

            self.insert_portfolio_object('Bittrex', balance_totals)

    # https://github.com/coinbase/coinbase-python
    # https://developers.coinbase.com/blog/2015/01/20/official-python-support
    def load_coinbase_accounts(self):
        for account_email, config in coinbase_accounts.iteritems():
            self.cb_client  = CB_Client(config['API_KEY'], config['API_SECRET'])
            cb_accounts = self.cb_client.get_accounts()['data'] # cb.Account Classes []

            summary = {}
            for acct in cb_accounts:
                curr = acct['balance']['currency']
                amount = acct['balance']['amount']
                summary[ curr ] = amount

            self.insert_portfolio_object('Coinbase', summary)

            ## CCXT does *not* support coinbase
            # coinbase = ccxt.coinbase({'apiKey':config['API_KEY'], 'secret':config['API_SECRET']})
            # balances = coinbase.fetchBalance()
            # summary = balances['total']

    def load_cryptopia_accounts(self):
        for account_email, config in cryptopia_accounts.iteritems():
            self.cryptopia = ccxt.cryptopia({'apiKey':config['API_KEY'], 'secret':config['API_SECRET'] })

            balances = self.cryptopia.fetchBalance()
            summary = balances['total']
            # Cryptopia returns all 0 balance entries. Filter them.
            summary_no_zero_balances = {k: v for k, v in summary.items() if v != 0}

            self.insert_portfolio_object('Cryptopia', summary_no_zero_balances)
            # print json.dumps(accounts, indent=2)r

    def load_gdax_accounts(self):
        for account_email, config in gdax_accounts.iteritems():
            self.gdax       = ccxt.gdax({'apiKey':config['API_KEY'], 'secret':config['API_SECRET'], 'password':config['passphrase']})

            balances = self.gdax.fetchBalance()
            summary = balances['total']

            self.insert_portfolio_object('GDAX', summary)
            # print json.dumps(accounts, indent=2)r

    def load_gemini_accounts(self):
        for account_email, config in gemini_accounts.iteritems():
            self.gemini     = ccxt.gemini({'apiKey':config['API_KEY'], 'secret':config['API_SECRET']})

            balances = self.gemini.fetchBalance()
            summary = balances['total']

            self.insert_portfolio_object('Gemini', summary)
            # print json.dumps(balances, indent=2)

    def get_sum_balances(self):
        sums = {}
        for exchange in PV.portfolio_info.keys():
            for account in PV.portfolio_info[exchange]:
                for coin in account.keys():

                    try:
                        # Don't count Leveraged Margin on Bitmex
                        if exchange=="Bitmex":
                            print("Not counting Bitmex margin stakes: "+str(account[coin]['used']))
                            self.bitmex_margin_stake += self.str_to_XBT( str(account[coin]['used']) )
                            coin_val = self.str_to_XBT( account[coin]['free'] )
                        else:
                            coin_val = self.str_to_XBT( account[coin] )

                        if coin in sums:
                            sums[coin] += coin_val
                        else:
                            sums[coin] = coin_val
                    except:
                        import pdb; pdb.set_trace()


        return sums

    @staticmethod
    def print_sums(sums):
        string_objs = {}
        for key in sums.keys():
            string_objs[key] = str(sums[key])
        print (json.dumps( string_objs,  indent=2))

    @staticmethod
    def str_to_XBT(XBT_str):
        return Decimal( XBT_str ).quantize(Decimal('.00000001'))

    def get_btc_usd_totals(self, balances):
        btc_total = Decimal(0)
        usd_total = Decimal(0)
        for key in balances.keys():
            # Skip tiny amounts (e.g. for Binance & Cryptopia forks/airdrops)
            if balances[key] < 1 and key not in ["BTC","XMR","ETH"]:
                print ("Skipping tiny coin: "+key)
                continue

            if key=="BTC":
                btc_total += balances[key]
                # import pdb; pdb.set_trace()
                print ("*%s: %s" % (key.rjust(4), str( round(balances[key],3))))
            elif key=="USD":
                usd_total += balances[key]
            elif key=="USDT":
                usd_total += balances[key]
            else:
                if key in ["1337", "IGNIS"]:
                    continue # LTC only pairing on cryptopia
                elif key in ["ETF"]:
                    continue
                # Query Binance for non-bittrex holdins
                elif key in ["APPC", "GTO","ENJ","TRX", "VEN","QSP","BNB","ZRX", "IOTA", "BQX"]: # Binance only non-bittrex coins
                    # self.binance.fetchTicker('TRX/BTC')
                    # import pdb; pdb.set_trace()
                    ticker = key+"/BTC"  # E.g. "ETH_BTC"
                    btc_rate = self.str_to_XBT( self.binance.fetchTicker(ticker)['last'] )
                    btc_value = balances[key] * btc_rate
                elif key in ["XBY", "LINDA", "GRWI", "SPANK"]:
                    ticker = key+"/BTC"  # E.g. "ETH_BTC"
                    btc_rate = self.str_to_XBT( self.cryptopia.fetchTicker(ticker)['last'] )
                    btc_value = balances[key] * btc_rate

                else:
                    ticker = key+"/BTC"  # E.g. "ETH/BTC"
                    try:
                        btc_rate = self.str_to_XBT( self.default_bittrex.fetchTicker(ticker)['last'] )
                    except:
                        btc_rate = self.str_to_XBT( self.cryptopia.fetchTicker(ticker)['last'] )

                    btc_value = balances[key] * btc_rate

                btc_rate_str = "%.8f" %  btc_rate
                btc_value_str = "%.8f" %  btc_value
                if (btc_value > 0.0002):
                    print ("%s: %s at %s BTC each is worth %s BTC" % (key.rjust(5), str(round(balances[key],2)).rjust(10), btc_rate_str, btc_value_str))
                btc_total+=btc_value

        return btc_total, usd_total

    def run(self, balances):
        print ("\n\nYour holdings in each account are: ")
        print (json.dumps(PV.portfolio_info,  indent=2))

        print ("\n\nYour summed holdings for each currency are: ")
        btc_total, usd_total = PV.get_btc_usd_totals(balances)
        # btc_price = manual_btc_price # Decimal('18900') # Placeholder value while BTC swings wildly on Dec 9th
        btc_price = PV.str_to_XBT( PV.gdax.fetchTicker('BTC/USD')['last'] )
        # import pdb; pdb.set_trace()
        btc_usd_value = (btc_total * btc_price)
        portfolio_value = btc_usd_value + usd_total

        portfolio_value_description_str = "%s BTC: ($%d) + $%d => %d" %( "%.3f"%btc_total, btc_usd_value, usd_total, portfolio_value)
        portfolio_btc_price_str = "GDAX BTC value: $%d" % ( round(btc_price,2) )

        runtime_str = datetime.datetime.now().strftime("%B %d, %Y: %I:%M%p ")
        self.output.write('\n\n'+ runtime_str + " -- "+portfolio_value_description_str)
        # self.output.write('\n' + "Your total Portfolio Value is estimated at: ")
        # self.output.write('\n' + portfolio_value_description_str)
        self.output.write('\n'+ portfolio_btc_price_str)
        self.output.write('\n'+ str(manual_holding_entries) )
        self.output.write('\n'+ str(total_deposits) )
        self.output.close()

        print ("\n\n" + runtime_str)
        print ("\n" + "Your total Portfolio Value is estimated at: ")
        print (portfolio_value_description_str)
        print (portfolio_btc_price_str)


    #     outside_assets = manual_holding_entries['James']
    # , "James"  : [{"BCH": -0.625,"LTC": -10,"USD":-10500}] # Approximate cash-value reduction
    # , "Greg"   : [{"USD":-1200}]
    # , "Matt"   : [{"USD":-2000}]

        deposits = sum( total_deposits.values() )
        profits = portfolio_value- Decimal(deposits)
        profit_pct = ((portfolio_value / Decimal(deposits))  -1)*100
        print ("\nYour total USD Deposits have been: $%d" % (deposits))
        print ("This yields a total profit of:  ** $%d ** (%d%%)"  % (profits, profit_pct))
        if PV.bitmex_margin_stake > 0:
            staked_usd = btc_price*PV.bitmex_margin_stake
            print ("Currently staked bitmex margin is %d, ($%d) for profit of $%d" % (PV.bitmex_margin_stake, staked_usd, profits+staked_usd))

        print ("\nThis is based on current holdings and price of those holdings when converted to BTC.")
        print ("So it is net of all transaction fees\n")

## ToDo: Trade history profit calculations
# class CryptoTradeHistory(CryptoPortfolio):
#     def __init__(self):
#         pass

#     def test(self):
#         print "Hi"
#         print "PV.portfolio_info"
#         pass

if __name__ == "__main__":
    try:
        PV = CryptoPortfolio()
        print ("Getting Balances")
        balances = PV.get_sum_balances()

        print ("Aggregating holdings and Calculating profits")
        PV.run(balances)
        ## Print holdings on each Exchange
        # print json.dumps(PV.portfolio_info,  indent=2)
        # PV.print_sums( balances )

    except:
        import pdb; pdb.set_trace()



