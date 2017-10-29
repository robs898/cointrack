import sqlite3
import yaml
import json
import requests
import pandas as pd
import os.path

def read_pb_yaml():
  with open("pb.yaml", 'r') as pb_coins_yaml:
    try:
      y = yaml.load(pb_coins_yaml)
      return y
    except yaml.YAMLError as exc:
      print(exc)

def populate(pb_coins, pb_type, cmc_coin_json):
  coin_list = []
  for pb_coin_symbol, pb_coin_limit in pb_coins.iteritems():
    for cmc_coin in cmc_coin_json:
      if pb_coin_symbol == cmc_coin['symbol']:
        price = float(cmc_coin['price_usd'])
        coin_info = {}
        coin_info['symbol'] = pb_coin_symbol
	roi = (float(pb_coin_limit) - price) / price
	coin_info['roi'] = round(roi, 2)
        coin_list.append(coin_info)
  return coin_list

def create_table(coins):
  coin_list = []
  for coin in coins:
      coin_list.append(coin['symbol'] + ' REAL')
  coin_sql = ', '.join(coin_list)
  db = sqlite3.connect('coinsdb')
  cursor = db.cursor()
  cursor.execute("CREATE TABLE coins(%s)" % coin_sql)
  db.commit()
  db.close()

def read_db():
  db = sqlite3.connect('coinsdb')
  cursor = db.cursor()
  cursor.execute('SELECT * FROM coins')
  return cursor.fetchall()

def check_db():
  try:
    db_contents = read_db()
    print(db_contents)
  except:
    print('coinsdb unreadable')
    raise

def populate_db(coins):
    coin_rois = []
    values = []
    for coin in coins:
        coin_rois.append(coin['roi'])
        values.append('?')
    values_sql = ', '.join(values)
    sql_string = "INSERT INTO coins VALUES (%s)" % values_sql
    db = sqlite3.connect('coinsdb')
    cursor = db.cursor()
    cursor.execute(sql_string, coin_rois)
    db.commit()
    db.close()

#get coins from pb yaml
pb_yaml = read_pb_yaml()
long_coins = pb_yaml['coins']['long']
short_coins = pb_yaml['coins']['short']

#get coins from cmc
cmc_request = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=200")
cmc_coin_list = cmc_request.content
cmc_coin_json = json.loads(cmc_coin_list)
btc_price = float(cmc_coin_json[0]['price_usd'])

#create arrays of coin dicts
long_coin_list = populate(long_coins, 'long', cmc_coin_json)
short_coin_list = populate(short_coins, 'short', cmc_coin_json)
all_coin_list = long_coin_list + short_coin_list

#create db if doesnt exist
if os.path.exists('coinsdb'):
  print('coindb already exists, continuing...')
else:
  create_table(all_coin_list)

#check db
check_db()

#populate db
populate_db(all_coin_list)

#check db
check_db()
