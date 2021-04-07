from flask import Flask, render_template, url_for, flash, redirect, request
from forms import Register, Login
import algo

app = Flask(__name__)

app.config["SECRET_KEY"] = 'b94517c1c47331d131b41d48435ec402'


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
       ticker = request.form["ticker"]
       return redirect(url_for('stock', tick= ticker))
    else:
       return render_template('home.html', )


@app.route('/<tick>', methods=['GET', 'POST'])
def stock(tick):
    pred, data = algo.time_series(tick)
    labels = [str(data.iloc[i,0]).strip("00:00:00") for i in range(0, 100, 1 )]
    legend = "CLOSE PRICE"
    values = [str(data.iloc[i,4]) for i in range(0, 100, 1 )]

    if request.method == "POST":
       data1 = request.form["ticker"]
       return redirect(url_for('stock', tick=data1))
    else:
       return render_template('stock.html',  pred = pred , labels=labels, legend=legend, values=values)


if __name__ == '__main__':
    app.run(debug=True)

    