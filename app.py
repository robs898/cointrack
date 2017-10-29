from flask import Flask, render_template, request
import pandas as pd
import pandas_highcharts.core
import sqlite3

app = Flask(__name__)

@app.route('/')
def graph_Example(chartID = 'chart_ID', chart_type = 'line', chart_height = 500):
    db = sqlite3.connect('coinsdb')
    df = pd.read_sql_query('SELECT * FROM coins', db)
    dataSet = pandas_highcharts.core.serialize(df, render_to='my-chart', output_type='json')
    return render_template('index.html', chart=dataSet)
