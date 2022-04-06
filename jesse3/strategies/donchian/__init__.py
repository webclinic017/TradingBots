from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils
from datetime import datetime

class donchian(Strategy):

    def toDatetime(self, tsms) -> str:
        ts = int(tsms)/1000
        return str(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%MZ'))
        
    def printst(self, event, period, utcDatetime, result : ta.donchian):
        print(f'{event} don-{period} dt={utcDatetime} {self.time} isLng={self.is_long} isSht={self.is_short} h={self.high:.1f} c={self.close:.1f} l={self.low:.1f} uband={result.upperband:.1f} mband={result.middleband:.1f} lband={result.lowerband:.1f}')

    def getTOCHL(self, candle):
        #print(candle)
        return candle[0], candle[1], candle[2], candle[3], candle[4]

    # Low level Donchain channel flat or rising
    # Candle Low < middle band
    # Candle Close > middle band
    def should_long(self) -> bool:
        ts, o, c, h, l = self.getTOCHL(self.candles[-1])
        result = ta.donchian(self.candles, period=20, sequential=False)
        middle = result.middleband
        shouldLong = l < middle and c > middle
        #if shouldLong:
        self.printst(f'should_long {shouldLong}', 20, self.toDatetime(ts), result)
        return shouldLong

    # High Level of Donchian Channel flat or falling
    # Candle High > middle band 
    # Candle Close < middle band
    def should_short(self) -> bool:
        print("len=", len(self.candles))
        ts, o, c, h, l = self.getTOCHL(self.candles[-1])
        print(f'should_short ts={ts} isLng={self.is_long} isSht={self.is_short} o={o:.1f} c={c:.1f} h={h:.1f} l={l:.1f}')
        print(f'should_short ts={self.time} isLng={self.is_long} isSht={self.is_short} o={self.open:.1f} c={self.close:.1f} h={self.high:.1f} l={self.low:.1f}')
        result = ta.donchian(self.candles, period=20, sequential=False)
        middle = result.middleband
        shouldShort = h > middle and c < middle
        #if shouldShort:
        self.printst(f'\nshould_short {shouldShort}', 20, self.toDatetime(ts), result)
        return shouldShort

    def should_cancel(self) -> bool:
        return True

    def go_long(self):
        # Open long position and use entire balance to buy
        qty = utils.size_to_qty(self.capital, self.price, fee_rate=self.fee_rate)

        self.buy = qty, self.price

    def go_short(self):
        # Open short position and use entire balance to sell
        qty = utils.size_to_qty(self.capital, self.price, fee_rate=self.fee_rate)

        self.sell = qty, self.price

    def update_position(self):
        pass

        # If there exist long position, but the signal shows Death Cross, then close the position, and vice versa.
        #if self.is_long and self.fast_sma < self.slow_sma:
        #    self.liquidate()
    
        #if self.is_short and self.fast_sma > self.slow_sma:
        #    self.liquidate()
