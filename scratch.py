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

def get_zip_info(zip_code):
    base_url = "https://www.zipcodeapi.com/rest/FokPyKZbaIf0lAHFjfGe3X5NkiGNfuZey430khU3HldnvthYpUGfbbpz30xE3udl/info.json"
    url = f"{base_url}/{zip_code}/degrees"

    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.content)
    else:
        return None


print(get_zip_info(56303)['state'])