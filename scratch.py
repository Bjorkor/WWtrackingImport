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
    j['tracks'][0]['carrier_code'] = 'Other'
    print(json.dumps(j))
    print(url)
