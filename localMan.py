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
import json
import pymongo
import traceback

global client
global db
global orders
import pyodbc
import pandas as pd

thread_local = local()
import re


def scrape():
    server = "WIN-PBL82ADEL98.HDLUSA.LAN,49816,49816"
    database = "HDL"
    driver_name = ''
    driver_names = [x for x in pyodbc.drivers()]
    if driver_names:
        driver_name = driver_names[0]
    if driver_name:
        conn_str = 'DRIVER={}; ...'.format(driver_name)
        # then continue with ...
        # pyodbc.connect(conn_str)
        # ... etc.

        try:
            cnxn = pyodbc.connect(driver=driver_name, server=server, database=database, trusted_connection='yes')
            cursor = cnxn.cursor()
            load_dotenv()
            dbaddr = os.getenv('DBADDR')
            client = pymongo.MongoClient(dbaddr)
            db = client["wwmongo"]
            orders = db["orders"]
        except pyodbc.Error as ex:
            msg = ex.args[1]
            if re.search('No Kerberos', msg):
                print('You must login using kinit before using this script.')
                exit(1)
            else:
                raise
    # SQL statements are executed using the Cursor execute() function.
    query = """select a.TransId, a.TrackingNum, s.[cf_External Trans Id] from tblSoShippingImport a join trav_tblSoTransHeader_view s on s.TransId = a.TransId"""
    cursor.execute(query)
    # Assigns all remaining rows to a list
    rows = cursor.fetchall()
    print('pulling data...')
    localMansPants = pd.read_sql(query, cnxn)
    print('data pulled')
    # Close the connection
    cnxn.close()

    localMansPants.rename(
        columns={"TransId": "traverse_id", "TrackingNum": "tracking", "cf_External Trans Id": "increment_id"},
        inplace=True)

    localMansPants = localMansPants.dropna()
    localMansPants = localMansPants[localMansPants['increment_id'].apply(lambda x: len(x) == 10)]
    localMansPants = localMansPants.astype({'increment_id': int})

    for index, row in localMansPants.iterrows():
        increment_id = row['increment_id']
        traverse_id = row['traverse_id']
        pullOrder(increment_id, traverse_id)
    try:
        qq = orders.find({'isTracked': False})
        orderMansPants = pd.DataFrame(list(qq))
        orderMansPants = orderMansPants[['entity_id', 'increment_id', 'dateCreated', 'dateModified', 'isTracked']]

        megazord = pd.merge(left=orderMansPants, right=localMansPants, on='increment_id', how='left')
        megazord['isTracked'] = True
        print('pushing tracking and traverse_id to database...')
        for index, row in megazord.iterrows():
            entity = row['entity_id']
            traverse_id = row['traverse_id']
            tracking = row['tracking']
            increment_id = row['increment_id']

            order(increment_id=increment_id).update('traverse_id', traverse_id)
            order(increment_id=increment_id).update('tracking', str(tracking))

    except:
        print('All orders in database have been tracked')


def pullOrder(increment_id, traverse_id):
    now = datetime.datetime.utcnow()
    target = now - datetime.timedelta(hours=2)
    # .strftime("%Y-%m-%d %H:%M:%S")

    load_dotenv()
    token = os.getenv('BEARER')
    headers = {'Authorization': f'Bearer {token}'}
    session = get_session()
    with session as session:
        api_url = f'https://wwhardware.com/rest/default/V1/orders?searchCriteria[pageSize]=1&searchCriteria[filterGroups][0][filters][0][field]=increment_id&searchCriteria[filterGroups][0][filters][0][value]={increment_id}'

        response = session.get(api_url, headers=headers)
        # print(response.status_code)
        # print(response.content)
        if response.status_code == 200:
            y = json.loads(response.content)
            try:
                entity_id = y['items'][0]['entity_id']
                order(entity_id=entity_id, increment_id=increment_id, traverse_id=traverse_id).new()
            except:
                pass
        if response.status_code == 400:
            print(response.content)
        if response.status_code != 200 and response.status_code != 400:
            # print('FFFFFF')
            while response.status_code != 200 and response.status_code != 400:
                print('retrying...')
                time.sleep(10)
                response = session.get(api_url, headers=headers)
                print(response.status_code)


def pushTracks():
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
        token = os.getenv('BEARER')
        headers = {'Authorization': f'Bearer {token}'}
        session = get_session()

        with session as session:

            response = session.post(url, headers=headers, json=json.dumps(j))
            # print(response.status_code)
            # print(response.content)
            if response.status_code == 200:
                y = json.loads(response.content)
                order(increment_id=increment).update('isTracked', True)
                print(f'Pushed tracking info for order {increment} to magento')
            if response.status_code == 400:
                print(f'order {increment} has an error')
                print(response.content)
            if response.status_code != 200 and response.status_code != 400:
                # print('FFFFFF')
                count = 0
                while response.status_code != 200 and response.status_code != 400:
                    if count < 6:
                        print(response.status_code)
                        print('retrying...')
                        time.sleep(10)
                        response = session.post(url, headers=headers, json=json.dumps(j))
                        count = count + 1
                    else:
                        pass


def get_session() -> Session:
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session
