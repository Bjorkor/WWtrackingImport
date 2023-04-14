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



df = pd.read_excel('WWMagentoTracking.xlsx')
col = ['magento', 'track', 'traverse']
df.fillna(value=11111111, inplace=True)
df.columns = col
for index, row in df.iterrows():
    pullOrder(row['magento'], row['traverse'])
    order(increment_id=row['magento']).update('tracking', str(row['track']))
pushTracks()