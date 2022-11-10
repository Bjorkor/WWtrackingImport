import sqlite3 as sl
import requests
from requests.sessions import Session
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, local
import time
import datetime
from dotenv import load_dotenv
import os
from orderMan import order
import localMan
import json
import pymongo
import traceback
global client
global db
global orders
import pyodbc
import pandas as pd
import re

thread_local = local()


def get_session() -> Session:
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session
j = '''{
  "tracks": 
    [
      {
        "track_number": null,
        "title": null,
        "carrier_code": null
      }
    ] 
}'''

trackFormats = ['']

j = json.loads(j)

load_dotenv()
dbaddr = os.getenv('DBADDR')
client = pymongo.MongoClient(dbaddr)
db = client["wwmongo"]
orders = db["orders"]

for x in orders.find({'isTracked': False}):
    tracknumber = str(x['tracking'])
    entity = x['entity_id']
    increment = x['increment_id']
    j['tracks'][0]['title'] = f'Order #{increment}'
    j['tracks'][0]['track_number'] = tracknumber
    url = f'https://wwhardware.com/rest/default/V1/order/{entity}/ship'
    if re.search(r'/\b(1Z ?[0-9A-Z]{3} ?[0-9A-Z]{3} ?[0-9A-Z]{2} ?[0-9A-Z]{4} ?[0-9A-Z]{3} ?[0-9A-Z]|[\dT]\d\d\d ?\d\d\d\d ?\d\d\d)\b/',tracknumber).span() is not None:
        j['tracks'][0]['carrier_code'] = 'UPS'
    elif re.search(r'/(\b96\d{20}\b)|(\b\d{15}\b)|(\b\d{12}\b)/', tracknumber).span() is not None or re.search(r'/\b((98\d\d\d\d\d?\d\d\d\d|98\d\d).span() ?\d\d\d\d ?\d\d\d\d( ?\d\d\d)?)\b/', tracknumber).span() is not None or re.search(r'/^[0-9]{15}$/', tracknumber).span() is not None:
        j['tracks'][0]['carrier_code'] = 'FedEx'
    elif re.search(r'/(\b\d{30}\b)|(\b91\d+\b)|(\b\d{20}\b)/', tracknumber).span() is not None or re.search(r'/^E\D{1}\d{9}\D{2}$|^9\d{15,21}$/', tracknumber).span() is not None or re.search(r'/^91[0-9]+$/', tracknumber).span() is not None or re.search(r'/^[A-Za-z]{2}[0-9]+US$/', tracknumber).span() is not None:
        j['tracks'][0]['carrier_code'] = 'USPS'
    else:
        j['tracks'][0]['carrier_code'] = 'Other'
    print(j['tracks'])
