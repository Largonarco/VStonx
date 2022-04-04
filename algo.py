from tickerstore.store import TickerStore
from datetime import date
import datetime
import pandas as pd
import talib

s_year = int(datetime.datetime.now().date().strftime("%Y"))
s_month = int(datetime.datetime.now().date().strftime("%m"))
s_date = int(datetime.datetime.now().date().strftime("%d"))

e_d =  datetime.datetime.now() + datetime.timedelta(days=-100)
e_year = int(e_d.date().strftime("%Y"))
e_month = int(e_d.date().strftime("%m"))
e_date = int(e_d.date().strftime("%d"))

def EMA(f):

    if f.iloc[0,0] > f.iloc[0,1] and f.iloc[1,0] < f.iloc[1,1]:
        a = 0
    elif f.iloc[0,0] < f.iloc[0,1] and f.iloc[1,0] > f.iloc[1,1]:
        a = 1
    elif f.iloc[0,0] >= f.iloc[0,1] - f.iloc[0,1]*0.07 and f.iloc[0,0] < f.iloc[0,1] + f.iloc[0,1]*0.07:
        a = 0
    elif f.iloc[0,1] >= f.iloc[0,0] - f.iloc[0,0]*0.07 and f.iloc[0,1] < f.iloc[0,0] + f.iloc[0,0]*0.07:
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

    if data.iloc[0,6] >= data["volume"].mean():
        d = 0
    else:
        d = 1

    return d

def TREND(data):
    if (data.iloc[0,5] - data.iloc[29,5])/30 > 1 :
        a = 1   
    elif (data.iloc[0,5] - data.iloc[29,5])/30 < -1 :
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

    fetcher = TickerStore()
    data = fetcher.historical_data(ticker, date(e_year,e_month,e_date), date(s_year,s_month,s_date),         TickerStore.INTERVAL_DAY_1)

    data = data.reset_index()
    data.rename(columns = {'Symbol':'Sym', 'Open':'open', 'Close':'close',
                              'High':'high', 'Low':'low', 'Volume':'volume'}, inplace = True)      
    data1 = data.iloc[::-1].head(130).reset_index(drop=True)
    data3 = data1.iloc[::-1]

    ema1 = talib.EMA(data['close'].values, 9)
    ema2 = talib.EMA(data['close'].values, 21)
    ema1 = pd.DataFrame(ema1, columns=['EMA1'])
    ema2 = pd.DataFrame(ema2, columns=['EMA2'])

    macd, macdsignal, macdhist = talib.MACD(data['close'], 12, 26, 9)
    macd = pd.DataFrame(macd, columns=['MACD']).reset_index(drop=True)
    macds = pd.DataFrame(macdsignal, columns=['MACDS']).reset_index(drop=True)   

    m_di = talib.MINUS_DI(data['high'], data[ 'low'], data['close'], timeperiod=14)
    p_di = talib.PLUS_DI(data['high'],  data[ 'low'], data['close'], timeperiod=14)
    m_di = pd.DataFrame(m_di, columns=['M_DI']).reset_index(drop=True)
    p_di = pd.DataFrame(p_di, columns=['P_DI']).reset_index(drop=True)

    output = ema1.join(ema2).join(macd).join(macds).join(m_di).join(p_di)
    output = output.iloc[::-1].reset_index(drop=True)

    e = PRED(data1, output)

    return e, data3, data1

def time_series_multi(ticker):
    data = []
    for i in ticker :
        ticker = i 
        e, data3, data1 = time_series(ticker)
        data.append(i+" : "+e)
    
    return data , data1

