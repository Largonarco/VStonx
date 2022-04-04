from nsetools import Nse

nse = Nse()

def gainers():
    gainers_list = []
    top_gainers = nse.get_top_gainers()

    for i in range(5):
        stock_name = top_gainers[i]['symbol']
        gainers_list.append(stock_name)

    return gainers_list


def losers():
    losers_list = []
    top_losers = nse.get_top_losers()

    for i in range(5):
        stock_name = top_losers[i]['symbol']
        losers_list.append(stock_name)

    return losers_list


def p_chng(ticker):
    data = []

    for i in ticker:
        ticker = i
        quote = nse.get_quote(ticker)
        p_chng = str(quote['pChange'])
        data.append(i+" : "+p_chng+"%")

    return data


def fundamentals(ticker):
    quote = nse.get_quote(ticker)
    high = str(quote['high52'])
    low = str(quote['low52'])
    f_value = str(quote['faceValue'])

    return high, low, f_value


def adv_dec():
    data = []

    e = nse.get_advances_declines()
    for d in e:
        if d == e[30]:
            for key in d:
                a = "{}".format(d[key])
                data.append(a)

    return data


def indices(ticker):
    quote = nse.get_index_quote(ticker)
    value = str(quote['lastPrice'])
    p_chng = str(quote['pChange'])

    return value, p_chng
