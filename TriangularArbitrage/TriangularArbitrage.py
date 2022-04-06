# "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\python.exe" triangulararbitrage.py

import pip._vendor.requests
import json

from collections import defaultdict

# Kraken US&Can not allow ETH2, GRT and FLOW
# Kraken AUD is VERY SLOW!
#EXCLUDED = ['ETH', 'ETH2', 'EWT', 'FLOW', 'XBT', 'YFI']
EXCLUDED = ['AUD', 'ETH2', 'EWT', 'FLOW', 'GRT', 'XBT', 'YFI']
FIATS = ['AUD', 'CHF', 'GBP', 'JPY', 'USD', 'USDT', 'SGD', 'MYR', 'CAD']
CRYPTO_FEE = 0.0015
FIAT_FEE = 0.002

TRIANGULAR_MIN_RATE = 1.02
FOURPOINT_MIN_RATE = 1.02

def isExcluded(c1, c2):
    if c1 in EXCLUDED or c2 in EXCLUDED:
        return True
    else:
        return False

def is4Excluded(c1, c2, c3, c4):
    if c1 in EXCLUDED or c2 in EXCLUDED or c3 in EXCLUDED or c4 in EXCLUDED:
        return True
    else:
        return False

def get_fee(c1, c2):
    if c1 in FIATS or c2 in FIATS:
        return FIAT_FEE
    else:
        return CRYPTO_FEE

s = pip._vendor.requests.Session() # use HTTP/1.1 to share the same connection across requests to minimise latency

# ----- COINUT SPOTS
#insts = s.post('http://api.coinut.com/', '{"request": "inst_list", "sec_type": "SPOT", "nonce": 1234}').json()
#while True:
#r = s.get('https://api.coinut.com/spot').json()


# ----- KRAKEN SPOTS
# https://www.kraken.com/features/api
# https://api.kraken.com/0/public/OHLC?pair=EOSETH&since=1619542765&interval=5
rates_request_url = 'https://api.kraken.com/0/public/Ticker?pair=AAVEAUD,AAVEETH,AAVEEUR,AAVEGBP,AAVEUSD,AAVEXBT,ADAAUD,ADAETH,ADAEUR,ADAGBP,ADAUSD,ADAUSDT,ADAXBT,ALGOETH,ALGOEUR,ALGOGBP,ALGOUSD,ALGOXBT,ANTETH,ANTEUR,ANTUSD,ANTXBT,ATOMAUD,ATOMETH,ATOMEUR,ATOMGBP,ATOMUSD,ATOMXBT,AUDJPY,AUDUSD,BALETH,BALEUR,BALUSD,BALXBT,BATETH,BATEUR,BATUSD,BATXBT,BCHAUD,BCHETH,BCHEUR,BCHGBP,BCHJPY,BCHUSD,BCHUSDT,BCHXBT,COMPETH,COMPEUR,COMPUSD,COMPXBT,CRVETH,CRVEUR,CRVUSD,CRVXBT,DAIEUR,DAIUSD,DAIUSDT,DASHEUR,DASHUSD,DASHXBT,DOTAUD,DOTETH,DOTEUR,DOTGBP,DOTUSD,DOTUSDT,DOTXBT,EOSETH,EOSEUR,EOSUSD,EOSUSDT,EOSXBT,ETHAUD,ETHCHF,ETHDAI,ETHUSDC,ETHUSDT,EURAUD,EURCAD,EURCHF,EURGBP,EURJPY,EWTEUR,EWTGBP,EWTUSD,EWTXBT,FILAUD,FILETH,FILEUR,FILGBP,FILUSD,FILXBT,FLOWETH,FLOWEUR,FLOWGBP,FLOWUSD,FLOWXBT,GNOETH,GNOEUR,GNOUSD,GNOXBT,GRTAUD,GRTETH,GRTEUR,GRTGBP,GRTUSD,GRTXBT,ICXETH,ICXEUR,ICXUSD,ICXXBT,KAVAETH,KAVAEUR,KAVAUSD,KAVAXBT,KEEPETH,KEEPEUR,KEEPUSD,KEEPXBT,KNCETH,KNCEUR,KNCUSD,KNCXBT,KSMAUD,KSMDOT,KSMETH,KSMEUR,KSMGBP,KSMUSD,KSMXBT,LINKAUD,LINKETH,LINKEUR,LINKGBP,LINKUSD,LINKUSDT,LINKXBT,LSKETH,LSKEUR,LSKUSD,LSKXBT,LTCAUD,LTCETH,LTCGBP,LTCUSDT,MANAETH,MANAEUR,MANAUSD,MANAXBT,NANOETH,NANOEUR,NANOUSD,NANOXBT,OCEANEUR,OCEANGBP,OCEANUSD,OCEANXBT,OMGETH,OMGEUR,OMGUSD,OMGXBT,OXTETH,OXTEUR,OXTUSD,OXTXBT,PAXGETH,PAXGEUR,PAXGUSD,PAXGXBT,QTUMETH,QTUMEUR,QTUMUSD,QTUMXBT,REPV2ETH,REPV2EUR,REPV2USD,REPV2XBT,SCETH,SCEUR,SCUSD,SCXBT,SNXAUD,SNXETH,SNXEUR,SNXGBP,SNXUSD,SNXXBT,STORJETH,STORJEUR,STORJUSD,STORJXBT,TBTCETH,TBTCEUR,TBTCUSD,TBTCXBT,TRXETH,TRXEUR,TRXUSD,TRXXBT,UNIETH,UNIEUR,UNIUSD,UNIXBT,USDCAUD,USDCEUR,USDCGBP,USDCHF,USDCUSD,USDCUSDT,USDTAUD,USDTCAD,USDTCHF,USDTEUR,USDTGBP,USDTJPY,USDTZUSD,WAVESETH,WAVESEUR,WAVESUSD,WAVESXBT,XBTAUD,XBTCHF,XBTDAI,XBTUSDC,XBTUSDT,XDGEUR,XDGUSD,XDGUSDT,XETCXETH,XETCXXBT,XETCZEUR,XETCZUSD,XETHXXBT,XETHZCAD,XETHZEUR,XETHZGBP,XETHZJPY,XETHZUSD,XLTCXXBT,XLTCZEUR,XLTCZJPY,XLTCZUSD,XMLNXETH,XMLNXXBT,XMLNZEUR,XMLNZUSD,XREPXETH,XREPXXBT,XREPZEUR,XREPZUSD,XRPAUD,XRPETH,XRPGBP,XRPUSDT,XTZAUD,XTZETH,XTZEUR,XTZGBP,XTZUSD,XTZXBT,XXBTZCAD,XXBTZEUR,XXBTZGBP,XXBTZJPY,XXBTZUSD,XXDGXXBT,XXLMXXBT,XXLMZAUD,XXLMZEUR,XXLMZGBP,XXLMZUSD,XXMRXXBT,XXMRZEUR,XXMRZUSD,XXRPXXBT,XXRPZCAD,XXRPZEUR,XXRPZJPY,XXRPZUSD,XZECXXBT,XZECZEUR,XZECZUSD,YFIAUD,YFIETH,YFIEUR,YFIGBP,YFIUSD,YFIXBT,ZEURZUSD,ZGBPZUSD,ZUSDZCAD,ZUSDZJPY'

kraken_pairs = """[{"a":"AAVEAUD","b":"AAVE","q":"AUD"},
{"a":"AAVEETH","b":"AAVE","q":"ETH"},
{"a":"AAVEEUR","b":"AAVE","q":"EUR"},
{"a":"AAVEGBP","b":"AAVE","q":"GBP"},
{"a":"AAVEUSD","b":"AAVE","q":"USD"},
{"a":"AAVEXBT","b":"AAVE","q":"XBT"},
{"a":"ADAAUD","b":"ADA","q":"AUD"},
{"a":"ADAETH","b":"ADA","q":"ETH"},
{"a":"ADAEUR","b":"ADA","q":"EUR"},
{"a":"ADAGBP","b":"ADA","q":"GBP"},
{"a":"ADAUSD","b":"ADA","q":"USD"},
{"a":"ADAUSDT","b":"ADA","q":"USDT"},
{"a":"ADAXBT","b":"ADA","q":"XBT"},
{"a":"ALGOETH","b":"ALGO","q":"ETH"},
{"a":"ALGOEUR","b":"ALGO","q":"EUR"},
{"a":"ALGOGBP","b":"ALGO","q":"GBP"},
{"a":"ALGOUSD","b":"ALGO","q":"USD"},
{"a":"ALGOXBT","b":"ALGO","q":"XBT"},
{"a":"ANTETH","b":"ANT","q":"ETH"},
{"a":"ANTEUR","b":"ANT","q":"EUR"},
{"a":"ANTUSD","b":"ANT","q":"USD"},
{"a":"ANTXBT","b":"ANT","q":"XBT"},
{"a":"ATOMAUD","b":"ATOM","q":"AUD"},
{"a":"ATOMETH","b":"ATOM","q":"ETH"},
{"a":"ATOMEUR","b":"ATOM","q":"EUR"},
{"a":"ATOMGBP","b":"ATOM","q":"GBP"},
{"a":"ATOMUSD","b":"ATOM","q":"USD"},
{"a":"ATOMXBT","b":"ATOM","q":"XBT"},
{"a":"AUDJPY","b":"AUD","q":"JPY"},
{"a":"AUDUSD","b":"AUD","q":"USD"},
{"a":"BALETH","b":"BAL","q":"ETH"},
{"a":"BALEUR","b":"BAL","q":"EUR"},
{"a":"BALUSD","b":"BAL","q":"USD"},
{"a":"BALXBT","b":"BAL","q":"XBT"},
{"a":"BATETH","b":"BAT","q":"ETH"},
{"a":"BATEUR","b":"BAT","q":"EUR"},
{"a":"BATUSD","b":"BAT","q":"USD"},
{"a":"BATXBT","b":"BAT","q":"XBT"},
{"a":"BCHAUD","b":"BCH","q":"AUD"},
{"a":"BCHETH","b":"BCH","q":"ETH"},
{"a":"BCHEUR","b":"BCH","q":"EUR"},
{"a":"BCHGBP","b":"BCH","q":"GBP"},
{"a":"BCHJPY","b":"BCH","q":"JPY"},
{"a":"BCHUSD","b":"BCH","q":"USD"},
{"a":"BCHUSDT","b":"BCH","q":"USDT"},
{"a":"BCHXBT","b":"BCH","q":"XBT"},
{"a":"COMPETH","b":"COMP","q":"ETH"},
{"a":"COMPEUR","b":"COMP","q":"EUR"},
{"a":"COMPUSD","b":"COMP","q":"USD"},
{"a":"COMPXBT","b":"COMP","q":"XBT"},
{"a":"CRVETH","b":"CRV","q":"ETH"},
{"a":"CRVEUR","b":"CRV","q":"EUR"},
{"a":"CRVUSD","b":"CRV","q":"USD"},
{"a":"CRVXBT","b":"CRV","q":"XBT"},
{"a":"DAIEUR","b":"DAI","q":"EUR"},
{"a":"DAIUSD","b":"DAI","q":"USD"},
{"a":"DAIUSDT","b":"DAI","q":"USDT"},
{"a":"DASHEUR","b":"DASH","q":"EUR"},
{"a":"DASHUSD","b":"DASH","q":"USD"},
{"a":"DASHXBT","b":"DASH","q":"XBT"},
{"a":"DOTAUD","b":"DOT","q":"AUD"},
{"a":"DOTETH","b":"DOT","q":"ETH"},
{"a":"DOTEUR","b":"DOT","q":"EUR"},
{"a":"DOTGBP","b":"DOT","q":"GBP"},
{"a":"DOTUSD","b":"DOT","q":"USD"},
{"a":"DOTUSDT","b":"DOT","q":"USDT"},
{"a":"DOTXBT","b":"DOT","q":"XBT"},
{"a":"EOSETH","b":"EOS","q":"ETH"},
{"a":"EOSEUR","b":"EOS","q":"EUR"},
{"a":"EOSUSD","b":"EOS","q":"USD"},
{"a":"EOSUSDT","b":"EOS","q":"USDT"},
{"a":"EOSXBT","b":"EOS","q":"XBT"},
{"a":"ETH2.SETH","b":"ETH2.S","q":"ETH"},
{"a":"ETHAUD","b":"ETH","q":"AUD"},
{"a":"ETHCHF","b":"ETH","q":"CHF"},
{"a":"ETHDAI","b":"ETH","q":"DAI"},
{"a":"ETHUSDC","b":"ETH","q":"USDC"},
{"a":"ETHUSDT","b":"ETH","q":"USDT"},
{"a":"EURAUD","b":"EUR","q":"AUD"},
{"a":"EURCAD","b":"EUR","q":"CAD"},
{"a":"EURCHF","b":"EUR","q":"CHF"},
{"a":"EURGBP","b":"EUR","q":"GBP"},
{"a":"EURJPY","b":"EUR","q":"JPY"},
{"a":"EWTEUR","b":"EWT","q":"EUR"},
{"a":"EWTGBP","b":"EWT","q":"GBP"},
{"a":"EWTUSD","b":"EWT","q":"USD"},
{"a":"EWTXBT","b":"EWT","q":"XBT"},
{"a":"FILAUD","b":"FIL","q":"AUD"},
{"a":"FILETH","b":"FIL","q":"ETH"},
{"a":"FILEUR","b":"FIL","q":"EUR"},
{"a":"FILGBP","b":"FIL","q":"GBP"},
{"a":"FILUSD","b":"FIL","q":"USD"},
{"a":"FILXBT","b":"FIL","q":"XBT"},
{"a":"FLOWETH","b":"FLOW","q":"ETH"},
{"a":"FLOWEUR","b":"FLOW","q":"EUR"},
{"a":"FLOWGBP","b":"FLOW","q":"GBP"},
{"a":"FLOWUSD","b":"FLOW","q":"USD"},
{"a":"FLOWXBT","b":"FLOW","q":"XBT"},
{"a":"GNOETH","b":"GNO","q":"ETH"},
{"a":"GNOEUR","b":"GNO","q":"EUR"},
{"a":"GNOUSD","b":"GNO","q":"USD"},
{"a":"GNOXBT","b":"GNO","q":"XBT"},
{"a":"GRTAUD","b":"GRT","q":"AUD"},
{"a":"GRTETH","b":"GRT","q":"ETH"},
{"a":"GRTEUR","b":"GRT","q":"EUR"},
{"a":"GRTGBP","b":"GRT","q":"GBP"},
{"a":"GRTUSD","b":"GRT","q":"USD"},
{"a":"GRTXBT","b":"GRT","q":"XBT"},
{"a":"ICXETH","b":"ICX","q":"ETH"},
{"a":"ICXEUR","b":"ICX","q":"EUR"},
{"a":"ICXUSD","b":"ICX","q":"USD"},
{"a":"ICXXBT","b":"ICX","q":"XBT"},
{"a":"KAVAETH","b":"KAVA","q":"ETH"},
{"a":"KAVAEUR","b":"KAVA","q":"EUR"},
{"a":"KAVAUSD","b":"KAVA","q":"USD"},
{"a":"KAVAXBT","b":"KAVA","q":"XBT"},
{"a":"KEEPETH","b":"KEEP","q":"ETH"},
{"a":"KEEPEUR","b":"KEEP","q":"EUR"},
{"a":"KEEPUSD","b":"KEEP","q":"USD"},
{"a":"KEEPXBT","b":"KEEP","q":"XBT"},
{"a":"KNCETH","b":"KNC","q":"ETH"},
{"a":"KNCEUR","b":"KNC","q":"EUR"},
{"a":"KNCUSD","b":"KNC","q":"USD"},
{"a":"KNCXBT","b":"KNC","q":"XBT"},
{"a":"KSMAUD","b":"KSM","q":"AUD"},
{"a":"KSMDOT","b":"KSM","q":"DOT"},
{"a":"KSMETH","b":"KSM","q":"ETH"},
{"a":"KSMEUR","b":"KSM","q":"EUR"},
{"a":"KSMGBP","b":"KSM","q":"GBP"},
{"a":"KSMUSD","b":"KSM","q":"USD"},
{"a":"KSMXBT","b":"KSM","q":"XBT"},
{"a":"LINKAUD","b":"LINK","q":"AUD"},
{"a":"LINKETH","b":"LINK","q":"ETH"},
{"a":"LINKEUR","b":"LINK","q":"EUR"},
{"a":"LINKGBP","b":"LINK","q":"GBP"},
{"a":"LINKUSD","b":"LINK","q":"USD"},
{"a":"LINKUSDT","b":"LINK","q":"USDT"},
{"a":"LINKXBT","b":"LINK","q":"XBT"},
{"a":"LSKETH","b":"LSK","q":"ETH"},
{"a":"LSKEUR","b":"LSK","q":"EUR"},
{"a":"LSKUSD","b":"LSK","q":"USD"},
{"a":"LSKXBT","b":"LSK","q":"XBT"},
{"a":"LTCAUD","b":"LTC","q":"AUD"},
{"a":"LTCETH","b":"LTC","q":"ETH"},
{"a":"LTCGBP","b":"LTC","q":"GBP"},
{"a":"LTCUSDT","b":"LTC","q":"USDT"},
{"a":"MANAETH","b":"MANA","q":"ETH"},
{"a":"MANAEUR","b":"MANA","q":"EUR"},
{"a":"MANAUSD","b":"MANA","q":"USD"},
{"a":"MANAXBT","b":"MANA","q":"XBT"},
{"a":"NANOETH","b":"NANO","q":"ETH"},
{"a":"NANOEUR","b":"NANO","q":"EUR"},
{"a":"NANOUSD","b":"NANO","q":"USD"},
{"a":"NANOXBT","b":"NANO","q":"XBT"},
{"a":"OCEANEUR","b":"OCEAN","q":"EUR"},
{"a":"OCEANGBP","b":"OCEAN","q":"GBP"},
{"a":"OCEANUSD","b":"OCEAN","q":"USD"},
{"a":"OCEANXBT","b":"OCEAN","q":"XBT"},
{"a":"OMGETH","b":"OMG","q":"ETH"},
{"a":"OMGEUR","b":"OMG","q":"EUR"},
{"a":"OMGUSD","b":"OMG","q":"USD"},
{"a":"OMGXBT","b":"OMG","q":"XBT"},
{"a":"OXTETH","b":"OXT","q":"ETH"},
{"a":"OXTEUR","b":"OXT","q":"EUR"},
{"a":"OXTUSD","b":"OXT","q":"USD"},
{"a":"OXTXBT","b":"OXT","q":"XBT"},
{"a":"PAXGETH","b":"PAXG","q":"ETH"},
{"a":"PAXGEUR","b":"PAXG","q":"EUR"},
{"a":"PAXGUSD","b":"PAXG","q":"USD"},
{"a":"PAXGXBT","b":"PAXG","q":"XBT"},
{"a":"QTUMETH","b":"QTUM","q":"ETH"},
{"a":"QTUMEUR","b":"QTUM","q":"EUR"},
{"a":"QTUMUSD","b":"QTUM","q":"USD"},
{"a":"QTUMXBT","b":"QTUM","q":"XBT"},
{"a":"REPV2ETH","b":"REPV2","q":"ETH"},
{"a":"REPV2EUR","b":"REPV2","q":"EUR"},
{"a":"REPV2USD","b":"REPV2","q":"USD"},
{"a":"REPV2XBT","b":"REPV2","q":"XBT"},
{"a":"SCETH","b":"SC","q":"ETH"},
{"a":"SCEUR","b":"SC","q":"EUR"},
{"a":"SCUSD","b":"SC","q":"USD"},
{"a":"SCXBT","b":"SC","q":"XBT"},
{"a":"SNXAUD","b":"SNX","q":"AUD"},
{"a":"SNXETH","b":"SNX","q":"ETH"},
{"a":"SNXEUR","b":"SNX","q":"EUR"},
{"a":"SNXGBP","b":"SNX","q":"GBP"},
{"a":"SNXUSD","b":"SNX","q":"USD"},
{"a":"SNXXBT","b":"SNX","q":"XBT"},
{"a":"STORJETH","b":"STORJ","q":"ETH"},
{"a":"STORJEUR","b":"STORJ","q":"EUR"},
{"a":"STORJUSD","b":"STORJ","q":"USD"},
{"a":"STORJXBT","b":"STORJ","q":"XBT"},
{"a":"TBTCETH","b":"TBTC","q":"ETH"},
{"a":"TBTCEUR","b":"TBTC","q":"EUR"},
{"a":"TBTCUSD","b":"TBTC","q":"USD"},
{"a":"TBTCXBT","b":"TBTC","q":"XBT"},
{"a":"TRXETH","b":"TRX","q":"ETH"},
{"a":"TRXEUR","b":"TRX","q":"EUR"},
{"a":"TRXUSD","b":"TRX","q":"USD"},
{"a":"TRXXBT","b":"TRX","q":"XBT"},
{"a":"UNIETH","b":"UNI","q":"ETH"},
{"a":"UNIEUR","b":"UNI","q":"EUR"},
{"a":"UNIUSD","b":"UNI","q":"USD"},
{"a":"UNIXBT","b":"UNI","q":"XBT"},
{"a":"USDCAUD","b":"USDC","q":"AUD"},
{"a":"USDCEUR","b":"USDC","q":"EUR"},
{"a":"USDCGBP","b":"USDC","q":"GBP"},
{"a":"USDCHF","b":"USD","q":"CHF"},
{"a":"USDCUSD","b":"USDC","q":"USD"},
{"a":"USDCUSDT","b":"USDC","q":"USDT"},
{"a":"USDTAUD","b":"USDT","q":"AUD"},
{"a":"USDTCAD","b":"USDT","q":"CAD"},
{"a":"USDTCHF","b":"USDT","q":"CHF"},
{"a":"USDTEUR","b":"USDT","q":"EUR"},
{"a":"USDTGBP","b":"USDT","q":"GBP"},
{"a":"USDTJPY","b":"USDT","q":"JPY"},
{"a":"USDTZUSD","b":"USDT","q":"USD"},
{"a":"WAVESETH","b":"WAVES","q":"ETH"},
{"a":"WAVESEUR","b":"WAVES","q":"EUR"},
{"a":"WAVESUSD","b":"WAVES","q":"USD"},
{"a":"WAVESXBT","b":"WAVES","q":"XBT"},
{"a":"XBTAUD","b":"XBT","q":"AUD"},
{"a":"XBTCHF","b":"XBT","q":"CHF"},
{"a":"XBTDAI","b":"XBT","q":"DAI"},
{"a":"XBTUSDC","b":"XBT","q":"USDC"},
{"a":"XBTUSDT","b":"XBT","q":"USDT"},
{"a":"XDGEUR","b":"XDG","q":"EUR"},
{"a":"XDGUSD","b":"XDG","q":"USD"},
{"a":"XDGUSDT","b":"XDG","q":"USDT"},
{"a":"XETCXETH","b":"ETC","q":"ETH"},
{"a":"XETCXXBT","b":"ETC","q":"XBT"},
{"a":"XETCZEUR","b":"ETC","q":"EUR"},
{"a":"XETCZUSD","b":"ETC","q":"USD"},
{"a":"XETHXXBT","b":"ETH","q":"XBT"},
{"a":"XETHZCAD","b":"ETH","q":"CAD"},
{"a":"XETHZEUR","b":"ETH","q":"EUR"},
{"a":"XETHZGBP","b":"ETH","q":"GBP"},
{"a":"XETHZJPY","b":"ETH","q":"JPY"},
{"a":"XETHZUSD","b":"ETH","q":"USD"},
{"a":"XLTCXXBT","b":"LTC","q":"XBT"},
{"a":"XLTCZEUR","b":"LTC","q":"EUR"},
{"a":"XLTCZJPY","b":"LTC","q":"JPY"},
{"a":"XLTCZUSD","b":"LTC","q":"USD"},
{"a":"XMLNXETH","b":"MLN","q":"ETH"},
{"a":"XMLNXXBT","b":"MLN","q":"XBT"},
{"a":"XMLNZEUR","b":"MLN","q":"EUR"},
{"a":"XMLNZUSD","b":"MLN","q":"USD"},
{"a":"XREPXETH","b":"REP","q":"ETH"},
{"a":"XREPXXBT","b":"REP","q":"XBT"},
{"a":"XREPZEUR","b":"REP","q":"EUR"},
{"a":"XREPZUSD","b":"REP","q":"USD"},
{"a":"XRPAUD","b":"XRP","q":"AUD"},
{"a":"XRPETH","b":"XRP","q":"ETH"},
{"a":"XRPGBP","b":"XRP","q":"GBP"},
{"a":"XRPUSDT","b":"XRP","q":"USDT"},
{"a":"XTZAUD","b":"XTZ","q":"AUD"},
{"a":"XTZETH","b":"XTZ","q":"ETH"},
{"a":"XTZEUR","b":"XTZ","q":"EUR"},
{"a":"XTZGBP","b":"XTZ","q":"GBP"},
{"a":"XTZUSD","b":"XTZ","q":"USD"},
{"a":"XTZXBT","b":"XTZ","q":"XBT"},
{"a":"XXBTZCAD","b":"XBT","q":"CAD"},
{"a":"XXBTZEUR","b":"XBT","q":"EUR"},
{"a":"XXBTZGBP","b":"XBT","q":"GBP"},
{"a":"XXBTZJPY","b":"XBT","q":"JPY"},
{"a":"XXBTZUSD","b":"XBT","q":"USD"},
{"a":"XXDGXXBT","b":"XDG","q":"XBT"},
{"a":"XXLMXXBT","b":"XLM","q":"XBT"},
{"a":"XXLMZAUD","b":"XLM","q":"AUD"},
{"a":"XXLMZEUR","b":"XLM","q":"EUR"},
{"a":"XXLMZGBP","b":"XLM","q":"GBP"},
{"a":"XXLMZUSD","b":"XLM","q":"USD"},
{"a":"XXMRXXBT","b":"XMR","q":"XBT"},
{"a":"XXMRZEUR","b":"XMR","q":"EUR"},
{"a":"XXMRZUSD","b":"XMR","q":"USD"},
{"a":"XXRPXXBT","b":"XRP","q":"XBT"},
{"a":"XXRPZCAD","b":"XRP","q":"CAD"},
{"a":"XXRPZEUR","b":"XRP","q":"EUR"},
{"a":"XXRPZJPY","b":"XRP","q":"JPY"},
{"a":"XXRPZUSD","b":"XRP","q":"USD"},
{"a":"XZECXXBT","b":"ZEC","q":"XBT"},
{"a":"XZECZEUR","b":"ZEC","q":"EUR"},
{"a":"XZECZUSD","b":"ZEC","q":"USD"},
{"a":"YFIAUD","b":"YFI","q":"AUD"},
{"a":"YFIETH","b":"YFI","q":"ETH"},
{"a":"YFIEUR","b":"YFI","q":"EUR"},
{"a":"YFIGBP","b":"YFI","q":"GBP"},
{"a":"YFIUSD","b":"YFI","q":"USD"},
{"a":"YFIXBT","b":"YFI","q":"XBT"},
{"a":"ZEURZUSD","b":"EUR","q":"USD"},
{"a":"ZGBPZUSD","b":"GBP","q":"USD"},
{"a":"ZUSDZCAD","b":"USD","q":"CAD"},
{"a":"ZUSDZJPY","b":"USD","q":"JPY"}]"""
pairs = json.loads(kraken_pairs)
#print (pairs[0]['a'])

#print (pairs[0]['a'])

# Search assets' "base" and "quote" ticker
def search_basequote (asset):
 for pairval in pairs:
   if pairval['a'] == asset:
     return pairval['b'], pairval['q']
 return None, None

while True:
    input("Press Enter to search pairs...")
    
    #kraken
    result = s.get(rates_request_url).json()['result']
    
    #binance
    #result = s.get(rates_request_url).json()
    
    curs = set()
    rates = defaultdict(dict)
    for asset in result:
        #print(asset)
        
        #kraken
        base, quote = search_basequote(asset)
        #print(base, quote, asset)

        #binance
        #base, quote = search_basequote(asset['symbol'])
        #print(base, quote, asset['symbol'])

        if not(base == None or quote == None):
            if not isExcluded(base, quote):
                curs.add(base)
                curs.add(quote)
        
                #kraken
                last_bid = float(result[asset]['c'][0])

                #binance
                #last_bid = float(asset['price'])

                rates[base][quote] = last_bid
                rates[quote][base] = 1.0/last_bid

    print ("Crypto fee:", CRYPTO_FEE, "$")
    print ("Fiat fee:", FIAT_FEE, "$")
    print ("Excluded assets:", EXCLUDED)

    print ("Triangular arbitrage opportunities > " + str(TRIANGULAR_MIN_RATE) + " -----------------------------------")
    for c1 in curs:
        for c2 in curs:
            for mid in curs:
                if c1 in rates and mid in rates and c2 in rates and mid in rates[c1] and c2 in rates[mid] and c1 in rates[c2]:
                    pair1_rate = rates[c1][mid] * (1-get_fee(c1, mid))
                    pair2_rate = rates[mid][c2] * (1-get_fee(mid, c2))
                    pair3_rate = rates[c2][c1] * (1-get_fee(c2, c1))
                    total_rate = pair1_rate * pair2_rate * pair3_rate
                    if total_rate > TRIANGULAR_MIN_RATE:
                        print ("%4s %4s %4s %15.8f %15.8f %15.8f %15.8f" % (c1, mid, c2, rates[c1][mid], rates[mid][c2], rates[c2][c1], total_rate))
                    #else:
                        #print ("!!! %4s %4s %4s %15.8f %15.8f %15.8f %15.8f" % (c1, mid, c2, rates[c1][mid], rates[mid][c2], rates[c2][c1], total_rate))

    #print ("Four-point arbitrage opportunities > " + str(FOURPOINT_MIN_RATE) + " -----------------------------------")
    #for c1 in curs:
    #    for c2 in curs:
    #        for c3 in curs:
    #            for c4 in curs:
    #                if c1 in rates and c2 in rates and c3 in rates and c2 in rates[c1] and c3 in rates[c2] and c4 in rates[c3] and c1 in rates[c4]:
    #                    pair1_rate = rates[c1][c2] * (1-get_fee(c1, c2))
    #                    pair2_rate = rates[c2][c3] * (1-get_fee(c2, c3))
    #                    pair3_rate = rates[c3][c4] * (1-get_fee(c3, c4))
    #                    pair4_rate = rates[c4][c1] * (1-get_fee(c4, c1))
    #                    total_rate = pair1_rate * pair2_rate * pair3_rate * pair4_rate

    #                    if total_rate > FOURPOINT_MIN_RATE:
    #                        print ("%4s %4s %4s %4s %15.8f %15.8f %15.8f %15.8f %15.8f" % (c1, c2, c3, c4, rates[c1][c2], rates[c2][c3], rates[c3][c4], rates[c4][c1], total_rate))
    ##                   #else:
    ##                   #print ("!!! %4s %4s %4s %4s %15.8f %15.8f %15.8f %15.8f %15.8f" % (c1, c2, c3, c4, rates[c1][c2], rates[c2][c3], rates[c3][c4], rates[c4][c1], total_rate))
