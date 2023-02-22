import sqlite3 as sl
import requests
from requests.sessions import Session
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, local
import time
import datetime
from dotenv import load_dotenv
import os
#from orderMan import order
#from orderMan import imports
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

token = os.getenv('BEARER')
headers = {'Authorization': f'Bearer {token}'}


def get_session() -> Session:
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session


def pullLocal():
    server = "WIN-PBL82ADEL98.HDLUSA.LAN,49816,49816"
    database = "HDL"
    driver_name = ''
    driver_names = [x for x in pyodbc.drivers()]
    if driver_names:
        driver_name = driver_names[0]
        if driver_name:
            conn_str = 'DRIVER={}; ...'.format(driver_name)

            try:
                cnxn = pyodbc.connect(driver=driver_name, server=server, database=database, trusted_connection='yes')
                cursor = cnxn.cursor()
            except pyodbc.Error as ex:
                msg = ex.args[1]
                if re.search('No Kerberos', msg):
                    print('You must login using kinit before using this script.')
                    exit(1)
                else:
                    raise
            dims = """SELECT  * FROM dbo.tblSHQdims"""
            lines = """SELECT  * FROM tblSoTransDetail"""
            header = """SELECT  * FROM tblSoTransHeader"""
            sku_uom = """select * from openquery ([HDL-WAREHOUSE],'select MASTER_STOCKNO,MASTER_REC_UT from wlib.dbo.master')"""
            query = sku_uom
            cursor.execute(query)

            rows = cursor.fetchall()
            print('pulling data...')
            df = pd.read_sql(query, cnxn)
            print('data pulled')
            cnxn.close()
            df.rename(columns={"MASTER_STOCKNO": "Product ID", "MASTER_REC_UT": "Unit"}, inplace=True)
            return df






load_dotenv()
dbaddr = os.getenv('DBADDR')
client = pymongo.MongoClient(dbaddr)
db = client["wwmongo"]
#wwimports = db["imports"]
variable_names = ['this_order_number', 'this_order_date', 'cfname', 'clname', 'baddone', 'baddtwo', 'ccity', 'cstate', 'czip', 'ccountry_code', 'hphone', 'this_email', 'sfname', 'slname', 'saddone', 'saddtwo', 'scity', 'sstate', 'szip', 'scountry_code', 'sphone', 'shipping', 'payment_type', 'ship_method', 'sku', 'qty', 'price', 'unit', 'tax_rate', 'promo_code', 'discount', 'comments', 'cut_list', 'cut_charge']
header = [
    'Order Number', 'Order Date', 'Customer Firstname', 'Customer Lastname', 'Customer Number',
    'Address 1', 'Address 2', 'City', 'State', 'Zip', 'Province/Other', 'Country', 'Home Phone',
    'Work Phone', 'Work Ext', 'Email', 'Ship Name', 'Ship Address 1', 'Ship Address 2', 'Ship City',
    'Ship State', 'Ship Zip', 'Ship Province/Other', 'Ship Country', 'Ship Phone', 'Product ID',
    'Quantity', 'Unit Price', 'Unit', 'Cut List', 'Cut Charge', 'Shipping Cost', 'Tax Rate',
    'Promotion Code', 'Discount', 'Shipping Method', 'Payment Type', 'Comments', 'Company Name'
]
#imports(Order_Number=1, Order_Date=datetime.datetime.utcnow()).imports()
df = pd.DataFrame(columns=header)
units = pullLocal()
session = get_session()
with session as session:
    api_url = 'https://wwhardware.com/rest/default/V1/orders?searchCriteria[pageSize]=1&searchCriteria[filterGroups][0][filters][0][field]=increment_id&searchCriteria[filterGroups][0][filters][0][value]=2000290713'

    response = session.get(api_url, headers=headers)
    # print(response.status_code)
    # print(response.content)
    if response.status_code == 200:
        y = json.loads(response.content)
        print(response.content)


        this_order_number = y['items'][0]['increment_id']
        this_order_date = y['items'][0]['created_at']
        cfname = y['items'][0]['billing_address']['firstname']
        clname = y['items'][0]['billing_address']['lastname']
        baddone = y['items'][0]['billing_address']['street'][0]
        if len(y['items'][0]['billing_address']['street']) > 1:
            baddtwo = y['items'][0]['billing_address']['street'][1]
        else:
            baddtwo = None
        ccity = y['items'][0]['billing_address']['city']
        cstate = y['items'][0]['billing_address']['region']
        czip = y['items'][0]['billing_address']['postcode']
        ccountry_code = y['items'][0]['billing_address']['country_id']

        hphone = y['items'][0]['billing_address']['telephone']
        this_email = y['items'][0]['billing_address']['email']
        sfname = y['items'][0]['extension_attributes']['shipping_assignments'][0]['shipping']['address']['firstname']
        slname = y['items'][0]['extension_attributes']['shipping_assignments'][0]['shipping']['address']['lastname']
        saddone = y['items'][0]['extension_attributes']['shipping_assignments'][0]['shipping']['address']['street'][0]
        if len(y['items'][0]['extension_attributes']['shipping_assignments'][0]['shipping']['address']['street']) > 1:
            saddtwo = y['items'][0]['extension_attributes']['shipping_assignments'][0]['shipping']['address']['street'][1]
        else:
            saddtwo = None
        scity = y['items'][0]['extension_attributes']['shipping_assignments'][0]['shipping']['address']['city']
        sstate = y['items'][0]['extension_attributes']['shipping_assignments'][0]['shipping']['address']['region']
        szip = y['items'][0]['extension_attributes']['shipping_assignments'][0]['shipping']['address']['postcode']
        scountry_code = y['items'][0]['extension_attributes']['shipping_assignments'][0]['shipping']['address']['country_id']
        sphone = y['items'][0]['extension_attributes']['shipping_assignments'][0]['shipping']['address']['telephone']
        shipping = y['items'][0]['shipping_invoiced']
        payment_type = y['items'][0]['payment']['method']
        ship_method = y['items'][0]['shipping_description']
        #co_name = y['items'][0]['extension_attributes']['shipping_assignments'][0]['shipping']['address']['company']
        for i in y['items'][0]['items']:
            sku = i['sku']
            qty = i['qty_ordered']
            price = i['base_price']
            unit = None
            tax_rate = i['base_tax_invoiced']
            promo_code = None
            discount = i['discount_invoiced']
            comments = None
            unit = None
            cut_list = None
            cut_charge = None
            if ccountry_code == 'US':
                order_dict = {
                    'Order Number': this_order_number,
                    'Order Date': this_order_date,
                    'Customer Firstname': cfname,
                    'Customer Lastname': clname,
                    'Customer Number': None,
                    'Address 1': baddone,
                    'Address 2': baddtwo,
                    'City': ccity,
                    'State': cstate,
                    'Zip': czip,
                    'Province/Other': None,
                    'Country': ccountry_code,
                    'Home Phone': hphone,
                    'Work Phone': None,
                    'Work Ext': None,
                    'Email': this_email,
                    'Ship Name': f"{sfname} {slname}",
                    'Ship Address 1': saddone,
                    'Ship Address 2': saddtwo,
                    'Ship City': scity,
                    'Ship State': sstate,
                    'Ship Zip': szip,
                    'Ship Province/Other': None,
                    'Ship Country': scountry_code,
                    'Ship Phone': sphone,
                    'Product ID': sku,
                    'Quantity': qty,
                    'Unit Price': price,
                    'Unit': unit,
                    'Cut List': cut_list,
                    'Cut Charge': cut_charge,
                    'Shipping Cost': shipping,
                    'Tax Rate': tax_rate,
                    'Promotion Code': promo_code,
                    'Discount': discount,
                    'Shipping Method': ship_method,
                    'Payment Type': payment_type,
                    'Comments': comments,
                    'Company Name': None
                }
            else:
                order_dict = {
                    'Order Number': this_order_number,
                    'Order Date': this_order_date,
                    'Customer Firstname': cfname,
                    'Customer Lastname': clname,
                    'Customer Number': None,
                    'Address 1': baddone,
                    'Address 2': baddtwo,
                    'City': ccity,
                    'State': None,
                    'Zip': czip,
                    'Province/Other': cstate,
                    'Country': ccountry_code,
                    'Home Phone': hphone,
                    'Work Phone': None,
                    'Work Ext': None,
                    'Email': this_email,
                    'Ship Name': f"{sfname} {slname}",
                    'Ship Address 1': saddone,
                    'Ship Address 2': saddtwo,
                    'Ship City': scity,
                    'Ship State': None,
                    'Ship Zip': szip,
                    'Ship Province/Other': cstate,
                    'Ship Country': scountry_code,
                    'Ship Phone': sphone,
                    'Product ID': sku,
                    'Quantity': qty,
                    'Unit Price': price,
                    'Unit': unit,
                    'Cut List': cut_list,
                    'Cut Charge': cut_charge,
                    'Shipping Cost': shipping,
                    'Tax Rate': tax_rate,
                    'Promotion Code': promo_code,
                    'Discount': discount,
                    'Shipping Method': ship_method,
                    'Payment Type': payment_type,
                    'Comments': comments,
                    'Company Name': None
                }
            order = pd.Series(order_dict)
            df = pd.concat([df, order.to_frame().T])
            print(sku)
    df = df.merge(right=pullLocal(), how='left', on='Product ID')
    df.to_csv('test.csv', index=False)
    print(df)




    if response.status_code == 400:
        print(response.content)
    if response.status_code != 200 and response.status_code != 400:
        # print('FFFFFF')
        while response.status_code != 200 and response.status_code != 400:
            print('retrying...')
            time.sleep(10)
            response = session.get(api_url, headers=headers)
            print(response.status_code)