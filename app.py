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
import re

load_dotenv()
dbaddr = os.getenv('DBADDR')
client = pymongo.MongoClient(dbaddr)
db = client["wwmongo"]
orders = db["orders"]

# .strftime("%Y-%m-%d %H:%M:%S")


thread_local = local()


def morehands() -> None:
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map()


def get_session() -> Session:
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session


try:
    localMan.scrape()
    localMan.pushTracks()
    for x in orders.find():
        print(order(x))

except:
    traceback.print_exc()
