
from jesse.strategies import Strategy
import jesse.indicators as jta
from jesse.helpers import slice_candles
from jesse import utils
from datetime import datetime
import numpy
import pandas as pd

#
# jesse backtest 2021-04-01 2021-05-01
#
class supertrendJesse(Strategy):
    period1 = 21
    multiplier1 = 4
    period2 = 21
    multiplier2 = 2

    supertrend = pd.DataFrame(columns=['timestamp', 'uband1', 'lband1', 'trendUp1', 'trendDown1', 'isUpTrend1', 'high', 'low', 'close', 'tr' ])
    supertrend['timestamp'] = pd.to_datetime(supertrend['timestamp'], unit='ms')

    def __init__(self):
        super().__init__()
        print("init.index=", len(self.supertrend.index))
        init = { 'timestamp': 0, 'uband1': 0, 'lband1': 0, 'trendUp1': 0, 'trendDown1': 0, 'isUpTrend1': 0, 'close': 0, 'high': 0, 'low': 0, 'tr': 0 }
        self.supertrend = self.supertrend.append(init, ignore_index=True)

    def tr(self, high, low, prevclose):
        hl = abs(high - low)
        hpc = abs(high - prevclose)
        lpc = abs(low - prevclose)
        return max(hl, hpc, lpc)

    def setSupertrend(self, candle):
        df = self.supertrend
        ts = candle[0]
        print("set.index=", len(df.index))
        current = len(df.index) - 1
        if ts > df['timestamp', current]:
            current = current + 1
            previous = current - 1
            df['timestamp'][current] = ts
            df['close'][current] = candle[2]
            df['high'][current] = candle[3]
            df['low'][current] = candle[4]
            df['tr'][current] = self.tr(df['high'][current], df['low'][current], df['close'][previous])

            atr1 = df['tr'].rolling(self.period1).mean()
            atr2 = df['tr'].rolling(self.period2).mean()

            source = (candle[3] + candle[4]) / 2
            df['uband1'][current] = source + atr1
            df['lband1'][current] = source - atr1
            df['isUpTrend1'][current] = True

            if df['close'][current] > df['uband1'][previous]:
                df['isUptrend1'][current] = True
            elif df['close'][current] < df['lband1'][previous]:
                df['isUptrend1'][current] = False
            else:
                df['isUptrend1'][current] = df['isUptrend1'][previous]
                if df['isUptrend1'][current] and df['lband1'][current] < df['lband1'][previous]:
                    df['lband1'][current] = df['lband1'][previous]
                if not df['isUptrend1'][current] and df['uband1'][current] > df['uband1'][previous]:
                    df['uband1'][current] = df['uband1'][previous]


    def toDatetime(self) -> str:
        ts = int(self.time)/1000
        return str(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%MZ'))

    # [0,1,2,3,4,5] [timestamp,open,close,high,low,volume]
    # self.current_candle[0]

    def printst(self, event, period, multiplier, utcDatetime, close, trend, changed):
        print(f'st-{period}-{multiplier} {event} dt={utcDatetime} close={close:.1f} trend={trend:.1f} changed={changed}')

    sequential = True
    
    #is buy signal
    def should_long(self) -> bool:
        #previous = self.candles[-1:]
        #print(previous)                

        trend, changed = jta.supertrend(self.candles, self.period1, self.multiplier1, self.sequential)
        print(f'changed={changed}')
        if changed == 1.0:
            self.printst("should_long", self.period1, self.multiplier1, self.toDatetime(), self.close, trend, changed)

        #trend, change = jta.supertrend(self.candles, self.period2, self.multiplier2, self.sequential)
        #if changed == 1.0:
        #    self.printst("should_long", self.period2, self.multiplier2, self.toDatetime(), self.close, trend, changed)

        return False 
    
    #is sell signal
    def should_short(self) -> bool:
        #print(f'len={len(self.candles)}')
        #previous = self.candles[-3:]
        #print(previous)

        candle = self.candles[0]
        print(f'candle={candle} datetime={self.toDatetime(candle[0])}')
        self.setSupertrend(candle)

        candle = self.candles[1]
        print(f'candle={candle} datetime={self.toDatetime(candle[0])}')
        
        candle = self.candles[-1]
        print(f'candle={candle} datetime={self.toDatetime(candle[0])}')


        trend, changed = jta.supertrend(self.candles, self.period1, self.multiplier1, self.sequential)
        print(f'changed={changed} len_changed={len(changed)}')
        if changed == 1.0:
            self.printst("should_short", self.period1, self.multiplier1, self.toDatetime(), self.close, trend, changed)

        #trend, change = jta.supertrend(self.candles, self.period2, self.multiplier2, self.sequential)
        #if changed == 1.0:
        #    self.printst("should_short", self.period2, self.multiplier2, self.toDatetime(), self.close, trend, changed)

        return False 

    def should_cancel(self) -> bool:
        return True

    def go_long(self):
        pass

    def go_short(self):
        pass
