import sqlite3
import yaml
import json
import requests
from pprint import pprint
import operator
import pandas as pd
import time

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
        coin_info['symbol'] = k
	coin_info['roi'] = (float(pb_coin_limit) - price / price)
        coin_list.append(coin_info)
  return coin_list

def get_cursor():
  db = sqlite3.connect('coinsdb')
  return db.cursor()

def create_table(coins):
  coin_list = []
  for coin in coins:
      coin_list.append(coin['symbol'] + ' TEXT')
  coin_sql = ', '.join(coin_list)
  cursor.execute("CREATE TABLE coins(time TEXT PRIMARY KEY, %s)" % coins)
  db.commit()

#get coins from pb yaml
pb_yaml = read_pb_yaml
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

print(all_coin_list)
