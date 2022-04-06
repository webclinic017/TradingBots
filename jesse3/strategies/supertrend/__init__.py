from jesse.strategies import Strategy
import jesse.indicators as jta
from jesse.helpers import slice_candles
from jesse import utils
from datetime import datetime
import numpy
import pandas as pd
import ta
import talib

#
# jesse backtest 2021-04-01 2021-05-01
# data window: plotchar(bar_index, "Bar Index", "", location = location.top)
class supertrend(Strategy):
    period1 = 7
    multiplier1 = 4
    period2 = 7
    multiplier2 = 2

    def toDatetime(self) -> str:
        ts = int(self.time)/1000
        return str(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%MZ'))

    def ta_atr(self, prefix, candles, period) -> float:
        #if self.atr != None:
        #    return self.atr

        atrdata = candles[-period:]
        #atrdata = slice_candles(self.candles, False)
        #print(f'prefix={prefix} atrdata=', atrdata)
        highs = pd.Series(atrdata[:,3])
        #print("highs=", highs)
        lows = pd.Series(atrdata[:,4])
        closes = pd.Series(atrdata[:,2])
        _atr = ta.volatility.AverageTrueRange(highs, lows, closes, period, False)
        _atrvalue = _atr.average_true_range().iloc[-1]
        #print (f'{prefix}_ta_atr={_atrvalue}')

        return _atrvalue
    
    def talib_atr(self, candles, period) -> float:
        #talib.ATR calculates ATR at period1+1
        #talibatrdata  = self.candles[-self.period1-2:-1:]
        talibatrdata = slice_candles(candles, False)
        #print("talibatrdata =", talibatrdata)
        highs = talibatrdata[:,3]
        lows = talibatrdata[:,4]
        closes = talibatrdata[:,2]
        #print("highs=", highs)
        # talib.ATR returns an array (rather than simple real)
        _talib_atr = talib.ATR(highs, lows, closes, period)
        print (f'_talib_atr={_talib_atr}')
        return _talib_atr

    def printst(self, event, period, multiplier, utcDatetime, close, trend, changed):
        print(f'st-{period}-{multiplier} {event} dt={utcDatetime} close={close:.1f} trend={trend:.1f} changed={changed}')

    #
    # uband = hl2 + (multiplier*atr(period))
    # lband = hl2 - (multiplier*atr(period))
    # tuband = close[1] < tuband[1] ? min(uBand, tuband[1]) : uBand
    # tlband = close[1] > tlband[1] ? max(lband, tlband[1]) : lband
    #
    # Trend = close > tuband[1] ? 1: close < tlband[1] ? -1 : nz(Trend[1], 1)
    # Tsl = Trend == 1 ? tlband : tuband
    #
    # [0,1,2,3,4,5] [timestamp,open,close,high,low,volume]
    # 

    def source(self, candle_row):
        #return (candle_row[3] + candle_row[4]) / 2 #hl2
        return candle_row[2] #close

    def upperBand(self, prefix, candles, period, multiplier) -> float:
        print(f'upperBand {prefix}c candles=', candles)
        curr_src = self.source(candles[-1])
        print(f'upperBand {prefix}c curr_src={curr_src:.1f}')
        curr_uband = curr_src + (multiplier * self.ta_atr(prefix+"c", candles, period))
        prev_candles = candles[-(period+1):-1]
        print(f'upperBand {prefix}p prev_candles=', prev_candles)
        prev_src = self.source(candles[-2])
        print(f'upperBand {prefix}p prev_src={prev_src:.1f}')
        prev_uband = prev_src + (multiplier * self.ta_atr(prefix+"p", prev_candles, period))
        prev_close = candles[-2,2]
        print(f'upperBand {prefix}p prev_close={prev_close:.1f} prev_uband={prev_uband:.1f} curr_uband={curr_uband:.1f}')
        return min(curr_uband, prev_uband) if (prev_close < prev_uband) else curr_uband

    def isDowntrend(self, prefix, candles, period, multiplier) -> bool:
        close = candles[-1, 2]
        uband = self.upperBand(prefix, candles, period, multiplier)
        print(f'isDowntrend {prefix} close={close:.1f} uband={uband:.1f}')
        return close < uband

    def lowBand(self, prefix, candles, period, multiplier) -> float:
        print(f'lowBand {prefix}c candles=', candles)
        curr_src = self.source(candles[-1])
        print(f'lowBand {prefix}c curr_src={curr_src:.1f}')
        curr_lband = curr_src - (multiplier * self.ta_atr(prefix+"c", candles, period))
        prev_candles = candles[-(period+1):-1]
        print(f'lowBand {prefix}p prev_candles=', prev_candles)
        prev_src = self.source(candles[-2])
        print(f'lowBand {prefix}p prev_src={prev_src:.1f}')
        prev_lband = prev_src + (multiplier * self.ta_atr(prefix+"p", prev_candles, period))
        prev_close = candles[-2, 2] 
        print(f'lowBand {prefix}p prev_close={prev_close:.1f} prev_lband={prev_lband:.1f} curr_lband={curr_lband:.1f}')
        return max(curr_lband, prev_lband) if (prev_close > prev_lband) else curr_lband

    def isUptrend(self, prefix, candles, period, multiplier) -> bool:
        close = candles[-1, 2]
        lband = self.lowBand(prefix, candles, period, multiplier)
        print(f'isUptrend {prefix} close={close:.1f} lband={lband:.1f}')
        return close > lband

    sequential = False
    atr = None

    #is buy signal
    def should_long(self) -> bool:
        print(f'len={len(self.candles)}')

        current = self.candles[-(self.period1+2):]
        #print(current)
        #self.atr = self.ta_atr("c", current, self.period1)
        #print("current ta.atr=", self.atr)

        previous = self.candles[-(self.period1+3):-1:]
        #print(previous)
        #self.atr = self.ta_atr("p", previous, self.period1)
        #print("previous ta.atr=", self.atr)
        
        print("should_long --------------")
        isDowntrend = self.isDowntrend("p", previous, self.period1, self.multiplier1) 
        isUptrend = self.isUptrend("c", current, self.period1, self.multiplier1)
        print(f'should_long isUptrend={isUptrend} isDowntrend={isDowntrend}')
        return isDowntrend and isUptrend
    
    #is sell signal
    # SuperTrend by KivancOzbilgic : hl2, 9, 3, ATR
    def should_short(self) -> bool:
        print(f'len={len(self.candles)}')
        print(self.candles)

        current = self.candles[-(self.period1+2):]
        #print("current=", current)
        #self.atr = self.ta_atr("c", current, self.period1)
        #print("current ta.atr=", self.atr)

        previous = self.candles[-(self.period1+3):-1:]
        #print("previous=", previous)
        #self.atr = self.ta_atr("p", previous, self.period1)
        #print("previous ta.atr=", self.atr)

        #self.atr = self.talib_atr()
        #print("talib.atr=", self.atr)

        #self.atr = jta.atr(self.candles, period1=self.period1, sequential=False)
        #print("jta.atr=", self.atr)

        print("should_short --------------")
        isUptrend = self.isUptrend("p", previous, self.period1, self.multiplier1)
        isDowntrend = self.isDowntrend("c", current, self.period1, self.multiplier1) 
        print(f'should_short isUptrend={isUptrend} isDowntrend={isDowntrend}')
        return isUptrend and isDowntrend

    def should_cancel(self) -> bool:
        return True

    def go_long(self):
        print("GO LONG!!!!!")
        return

    def go_short(self):
        print("GO SHORT!!!!!")
        return
