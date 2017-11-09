from flask import Flask, render_template, request
import pandas as pd
import pandas_highcharts.core
import sqlite3

app = Flask(__name__)

@app.route('/')
def graph():
    db = sqlite3.connect('coinsdb')
    df = pd.read_sql_query('SELECT * FROM coins', db)
    dataSet = pandas_highcharts.core.serialize(df, render_to='my-chart', output_type='json', title="Longs", ylim=[-0.25,2], figsize=(1000,1000))
    return render_template('index.html', chart=dataSet)
