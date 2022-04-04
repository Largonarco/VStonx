from flask import Flask, render_template, url_for, flash, redirect, request
from forms import SearchForm, DropdownForm
import algo, gainers_losers

app = Flask(__name__)

app.config["SECRET_KEY"] = 'b94517c1c47331d131b41d48435ec402'


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    stock = SearchForm(request.form)

    g_list = gainers_losers.gainers()
    l_list = gainers_losers.losers()
    gainers = gainers_losers.p_chng(g_list)
    losers = gainers_losers.p_chng(l_list)
    adv_dec = gainers_losers.adv_dec()
    advance = adv_dec[1]
    decline = adv_dec[2]
    u_changed = adv_dec[3]
    n_value, n_chng = gainers_losers.indices("NIFTY 50")
    return render_template('home.html', form=stock, gainers=gainers, losers=losers, advance=advance, decline=decline, u_changed=u_changed,
                            n_value=n_value, n_chng=n_chng)



@app.route('/<tick>', methods=['GET', 'POST'])
def stock(tick):
    stock = SearchForm(request.form)

    pred, data3, data1 = algo.time_series(tick)
    labels = [str(data3.iloc[i, 0]).strip("00:00:00") for i in range(0, 130, 1)]
    legend = tick
    values = [str(data3.iloc[i, 5]) for i in range(0, 130, 1)]
    p_chng = round(((data1.iloc[0, 5] - data1.iloc[1, 5]) / data1.iloc[1, 5])*100, 2)
    high, low, f_value = gainers_losers.fundamentals(tick)

    if request.method == 'POST' and stock.validate_on_submit():
        ticker = stock.search.data
        ticker = ticker.upper()
        return redirect(url_for('stock', tick=ticker, form=stock))
    else:
        return render_template('stock.html',  pred=pred, labels=labels, legend=legend, values=values, ticker=tick, p_chng=p_chng,
                               high=high, low=low, f_value=f_value, form=stock)



@app.route('/index_search', methods=['GET', 'POST'])
def search():
    dropdown = DropdownForm(request.form)

    if request.method == 'POST' and dropdown.validate_on_submit():
        index = dropdown.index.data
        if index == "NIFTY50":
            stocks = ["ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BHARTIARTL", "BPCL", "CIPLA", "COALINDIA", "DRREDDY", "EICHERMOT", "GAIL", "GRASIM", "HCLTECH", "HDFC", "HDFCBANK", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "BRITANNIA",
                      "ICICIBANK", "INDUSINDBK", "INFY", "IOC", "ITC", "JSWSTEEL", "KOTAKBANK", "LT", "MARUTI", "NESTLEIND", "NTPC", "ONGC", "POWERGRID", "SBIN", "SUNPHARMA", "TCS", "TATAMOTORS", "TATASTEEL", "TECHM", "TITAN", "ULTRACEMCO", "UPL", "WIPRO", "SHREECEM", "DIVISLAB"]
            data, data1 = algo.time_series_multi(stocks)
            return render_template('index_search.html', form_1=dropdown, data=data, selection=index)
        elif index == "NIFTY_M50":
            stocks = ['APOLLOHOSP', 'ALKEM',  'ADANIPOWER', 'AMARAJABAT', 'APOLLOTYRE', 'ASHOKLEY', 'BALKRISIND', 'BANKBARODA', 'BANKINDIA', 'BATAINDIA', 'BEL', 'BHARATFORG', 'BHEL', 'CANBK', 'CESC', 'CHOLAFIN', 'CUMMINSIND', 'ESCORTS', 'EXIDEIND', 'FEDERALBNK', 'GMRINFRA', 'GLENMARK',
                      'GODREJPROP', 'IDEA', 'IBULHSGFIN', 'JINDALSTEL', 'JUBLFOOD', 'LICHSGFIN', 'MGL', 'MRF', 'MFSL', 'MINDTREE', 'NATIONALUM', 'OIL', 'RBL', 'RECLTD', 'RAMCOCEM', 'SRF', 'SAIL', 'SUNTV', 'TATACHEM', 'TVSMOTOR', 'TATAPOWER', 'TORNTPOWER', 'UNIONBANK',  'VOLTAS', 'YESBANK']
            data, data1 = algo.time_series_multi(stocks)
            return render_template('index_search.html', form_1=dropdown, data=data, selection=index)
        elif index == "NIFTY_S50":
            stocks = ['ASHOKA', 'BAJAJELEC', 'BEML',  'BLUESTARCO', 'CENTURYPLY', 'CEATLTD', 'COCHINSHIP', 'DCBBANK', 'DEEPAKNTR', 'DBL', 'EIDPARRY', 'FSL', 'GMMPFAUDLR', 'GODFRYPHLP', 'GRAPHITE', 'GUJALKALI', 'HSCL', 'IDFC', 'IBREALEST', 'INFIBEAM', 'ITI', 'JMFINANCIL', 
                    'KAJARIACER', 'KARURVYSYA', 'KEC', 'LAXMIMACH', 'LEMONTREE', 'LUXIND', 'METROPOLIS', 'MMTC', 'MOIL', 'NBCC', 'OMAXE', 'PNCINFRA', 'RVNL', 'RALLIS', 'RAYMOND', 'SOBHA', 'SPICEJET', 'STAR', 'SUNTECK', 'TIMKEN', 'VAKRANGEE',  'WELCORP', 'WOCKPHARMA']
            data, data1 = algo.time_series_multi(stocks)
            return render_template('index_search.html', form_1=dropdown, data=data, selection=index)
    else:
        return render_template('index_search.html', form_1=dropdown)


if __name__ == '__main__':
    app.run(debug=True)
