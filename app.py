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


try:
    localMan.scrape()
    localMan.pushTracks()


except:
    traceback.print_exc()
