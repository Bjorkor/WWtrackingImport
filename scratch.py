import sqlite3 as sl
import requests
from requests.sessions import Session
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, local
import time
import datetime
from dotenv import load_dotenv
import os
from localMan import scrape
from localMan import pushTracks
from localMan import pullOrder
import json
import pymongo
from orderMan import order
import traceback
global client
global db
global orders
import pyodbc
import pandas as pd
thread_local = local()
import re

load_dotenv()
dbaddr = os.getenv('DBADDR')
client = pymongo.MongoClient(dbaddr)
db = client["wwmongo"]
orders = db["orders"]

order_numbers = [2000310276, 2000310450, 2000310450, 2000310426, 2000310426, 2000310462, 2000310462, 2000310183, 2000310183, 2000310465]
for x in order_numbers:
    print(orders.find_one({"traverse_id": x}))
