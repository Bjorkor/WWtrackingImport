import pandas as pd
import pymongo
import requests
from dotenv import load_dotenv
import os
import datetime
from orderMan import order
import json
from requests.sessions import Session
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, local
import time


def get_session() -> Session:
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session


thread_local = local()
now = datetime.datetime.utcnow()
target = now - datetime.timedelta(hours=2)
# .strftime("%Y-%m-%d %H:%M:%S")

load_dotenv()
token = os.getenv('BEARER')
headers = {'Authorization': f'Bearer {token}'}
session = get_session()
list = ['2000301013', '2000301012', '2000301011', '2000301010', '', '2000301009']

for increment_id in list:
    with session as session:
        api_url = f'https://wwhardware.com/rest/default/V1/orders?searchCriteria[pageSize]=1&searchCriteria[filterGroups][0][filters][0][field]=increment_id&searchCriteria[filterGroups][0][filters][0][value]={increment_id}'

        response = session.get(api_url, headers=headers)
        # print(response.status_code)
        # print(response.content)
        if response.status_code == 200:
            #y = json.loads(response.content)
            y = response.content
            for x in y['items']:
                print(x)
                # time.sleep(5)
        if response.status_code == 400:
            print(response.content)
        if response.status_code != 200 and response.status_code != 400:
            # print('FFFFFF')
            while response.status_code != 200 and response.status_code != 400:
                print('retrying...')
                time.sleep(10)
                response = session.get(api_url, headers=headers)
                print(response.status_code)