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
load_dotenv()
dbaddr = os.getenv('DBADDR')
client = pymongo.MongoClient(dbaddr)
db = client["wwmongo"]
orders = db["orders"]

# .strftime("%Y-%m-%d %H:%M:%S")



thread_local = local()



def pullOrders():
    now = datetime.datetime.utcnow()
    target = now - datetime.timedelta(hours=2)
    # .strftime("%Y-%m-%d %H:%M:%S")
    api_url = f'https://wwhardware.com/rest/default/V1/orders?searchCriteria[sortOrders][0][field]=created_at&searchCriteria[sortOrders][0][direction]=DESC&searchCriteria[filterGroups][0][filters][0][conditionType]=gteq&searchCriteria[filterGroups][0][filters][0][field]=created_at&searchCriteria[filterGroups][0][filters][0][value]={target.strftime("%Y-%m-%d %H:%M:%S")}'

    load_dotenv()
    token = os.getenv('BEARER')
    headers = {'Authorization': f'Bearer {token}'}
    session = get_session()
    with session as session:
        response = session.get(api_url, headers=headers)
        #print(response.status_code)
        #print(response.content)
        if response.status_code == 200:
            y = json.loads(response.content)
            for x in y['items']:
                entity = int(x['entity_id'])
                increment = int(x['increment_id'])
                order(entity_id=entity, increment_id=increment).new()
                #time.sleep(5)
        if response.status_code == 400:
            print(response.content)
        if response.status_code != 200 and response.status_code != 400:
            # print('FFFFFF')
            while response.status_code != 200 and response.status_code != 400:
                print('retrying...')

                response = session.get(api_url, headers=headers)
                print(response.status_code)
    localMan.scrape()

def morehands() -> None:
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map()


def get_session() -> Session:
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session

#pullOrders()
try:
    orders.drop()

except:
    traceback.print_exc()


