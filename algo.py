from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import pandas as pd
import talib

def EMA(f):

    if f.iloc[0,0] > f.iloc[0,1] and f.iloc[1,0] < f.iloc[1,1]:
        a = 0
    elif f.iloc[0,0] < f.iloc[0,1] and f.iloc[1,0] > f.iloc[1,1]:
        a = 1
    elif f.iloc[0,0] >= f.iloc[0,1] - f.iloc[0,1]*0.02:
        a = 0
    elif f.iloc[0,1] >= f.iloc[0,0] - f.iloc[0,0]*0.02:
        a = 1
    else:
        a = 2
     
    return a

def MACD (data):

     if data.iloc[0,2] > data.iloc[0,3] :
        b = 0
     elif data.iloc[0,2] < data.iloc[0,3] :
        b = 1

     return b

def ADX (data):

    if data.iloc[0,5] > data.iloc[0,4]:
        c = 0
    elif data.iloc[0,5] >= data.iloc[0,4] - data.iloc[0,4]*0.05:
        c = 0
    elif data.iloc[0,4] >= data.iloc[0,5] - data.iloc[0,5]*0.05:
        c = 1
    elif data.iloc[0,4] < data.iloc[0,5]:
        c = 1
    else:
        c = 0

    return c

def VOL (data):

    if data.iloc[0,5] >= data["volume"].mean():
        d = 0
    else:
        d = 1

    return d

def TREND(data):
    if (data.iloc[0,4] - data.iloc[29,4])/30 > 1 :
        a = 1   
    elif (data.iloc[0,4] - data.iloc[29,4])/30 < -1 :
        a = 0  
    else:
        a = 2
    
    return a

def PRED (data, output):
    a = EMA(output)
    b = MACD(output)
    c = ADX(output)
    d = VOL(data)
    e = TREND(data)

    if a == 2 :
        f = "NO ACTION"
    elif a == b == c == d == e == 0 : 
        f = "STRONG BUY" 
    elif a == b == c == d == e == 1  :
        f = "STRONG SELL"       
    elif a == b == c == e == 0  :
        f = "BUY"
    elif a == b == c == e == 1  :
        f = "SELL"  
    else:
        f = "NO ACTION"
              
    return f



def time_series(ticker):

    ts = TimeSeries(key='2NEU7G5UZDPRRN3I', output_format='pandas')
    data, meta_data = ts.get_daily(symbol=ticker, outputsize='compact')

    data = data.reset_index()
    data.rename(columns = {'1. open':'open', '4. close':'close',
                              '2. high':'high', '3. low':'low', '5. volume':'volume'}, inplace = True)      
    data1 = data.iloc[::-1]

    ema1 = talib.EMA(data1['close'].values, 9)
    ema2 = talib.EMA(data1['close'].values, 21)
    ema1 = pd.DataFrame(ema1, columns=['EMA1'])
    ema2 = pd.DataFrame(ema2, columns=['EMA2'])

    macd, macdsignal, macdhist = talib.MACD(data1['close'], 12, 26, 9)
    macd = pd.DataFrame(macd, columns=['MACD']).reset_index(drop=True)
    macds = pd.DataFrame(macdsignal, columns=['MACDS']).reset_index(drop=True)   

    m_di = talib.MINUS_DI(data1['high'], data1[ 'low'], data1['close'], timeperiod=14)
    p_di = talib.PLUS_DI(data1['high'],  data1[ 'low'], data1['close'], timeperiod=14)
    m_di = pd.DataFrame(m_di, columns=['M_DI']).reset_index(drop=True)
    p_di = pd.DataFrame(p_di, columns=['P_DI']).reset_index(drop=True)

    output = ema1.join(ema2).join(macd).join(macds).join(m_di).join(p_di)
    output = output.iloc[::-1].reset_index(drop=True)

    e = PRED(data, output)

    return e, data1
