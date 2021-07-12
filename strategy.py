from config import *
import ccxt
import pandas as pd
import talib
import numpy as np

#Data 
def strategy(crypto, type, security): 
    global key, secret

    #reseting buy trigger and strategytype
    security = 0
    type = 0

    exchange = ccxt.binance({ 
        'apiKey': key, 
        'secret': secret, 
    }) 

    bars = exchange.fetch_ohlcv(crypto, limit=100) 

    df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']) 

    close = np.array(df['close'])

    #Indicators 

    #Bollingerbands 
    upperband, middleband, lowerband = talib.BBANDS(close, timeperiod=5, nbdevup=2, matype=0) 
    if lowerband[-1] > close[-1]:
        security += 1
        type = 'Bollinger Bands'
    elif upperband[-1] < close[-1]: 
        security -= 1 
    else:
        security *= 1

    #Rsi-Index 
    rsi_value = talib.RSI(close, timeperiod=14) 

    if rsi_value[-1] < 30:
        security += 1
        type = 'RSI Index' 
    elif rsi_value[-1] >= 70:
        security -= 1
    else:
        security *= 1

    #MACD 
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9) 

    if macd[-1] >= macdsignal[-1] and macdhist[-1] >= 0 and macdhist[-1] < 0.03:
        security += 1
        type = 'MACD' 
    elif macd[-1] <= macdsignal[-1] and macdhist[-1] <= 0 and macdhist[-1] < 0.03:
        security -= 1
    else:
        security *= 1

    #Average True Range 
    # atr_value = talib.ATR(np.array(df['high']), np.array(df['low']), np.array(close), timeperiod=14) 
    # print(atr_value) 

    #Moving Average (long buy)
    ma_value = talib.MA(close, timeperiod=30, matype=0) 

    difference = close[-1] * 0.95

    if ma_value[-1] <= close[-1] and ma_value[-1] >= difference:
        security += 1
        type = 'MA' 
    else:
        security *= 1
    
    return security



