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
    'Quantity', 'Unit Price', 'Cut List', 'Cut Charge', 'Shipping Cost', 'Tax Rate',
    'Promotion Code', 'Discount', 'Shipping Method', 'Payment Type', 'Comments', 'Company Name'
]
header2 = ["Order Number", "Order Date", "Customer Firstname", "Customer Lastname", "Customer Number", "Address 1", "Address 2", "City", "State", "Zip", "Province/Other", "Country", "Home Phone", "Work Phone", "Work Ext", "Email", "Ship Name", "Ship Address 1", "Ship Address 2", "Ship City", "Ship State", "Ship Zip", "Ship Province/Other", "Ship Country", "Ship Phone", "Product ID", "Quantity", "Unit Price", "Unit", "Cut List", "Cut Charge", "Shipping Cost", "Tax Rate", "Promotion Code", "Discount", "Shipping Method", "Payment Type", "Comments", "Company", "RepId", "ShipAtt"]

#imports(Order_Number=1, Order_Date=datetime.datetime.utcnow()).imports()
df = pd.DataFrame(columns=header2)
units = pullLocal()
session = get_session()
with session as session:
    api_url = 'https://wwhardware.com/rest/default/V1/orders?searchCriteria[pageSize]=1&searchCriteria[filterGroups][0][filters][0][field]=increment_id&searchCriteria[filterGroups][0][filters][0][value]=2000307418'
    api_url_proc = 'https://wwhardware.com/rest/default/V1/orders?searchCriteria[pageSize]=1000&searchCriteria[filterGroups][0][filters][0][field]=status&searchCriteria[filterGroups][0][filters][0][value]=processing'



    response = session.get(api_url_proc, headers=headers)
    # print(response.status_code)
    # print(response.content)
    if response.status_code == 200:
        yres = json.loads(response.content)
        #print(response.content)

        for y in yres['items']:
            this_order_number = y['increment_id']
            this_order_date = y['created_at']
            cfname = y['billing_address']['firstname']
            clname = y['billing_address']['lastname']
            baddone = y['billing_address']['street'][0]
            if len(y['billing_address']['street']) > 1:
                baddtwo = y['billing_address']['street'][1]
            else:
                baddtwo = None
            ccity = y['billing_address']['city']
            cstate = y['billing_address']['region']
            czip = y['billing_address']['postcode']
            ccountry_code = y['billing_address']['country_id']

            hphone = y['billing_address']['telephone']
            this_email = y['billing_address']['email']
            sfname = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['firstname']
            slname = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['lastname']
            saddone = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['street'][0]
            if len(y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['street']) > 1:
                saddtwo = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['street'][1]
            else:
                saddtwo = None
            scity = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['city']
            sstate = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['region']
            szip = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['postcode']
            scountry_code = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['country_id']
            sphone = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['telephone']
            shipping = y['shipping_invoiced']
            payment_type = y['payment']['method']
            ship_method = y['shipping_description']
            #co_name = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['company']
            icount = 0
            for i in y['items']:
                sku = i['sku']
                qty = i['qty_ordered']
                price = i['base_price']
                unit = None
                tax_rate = 0
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
                if icount == 0:
                    order_dict['Tax Rate'] = y['items'][0]['tax_invoiced']
                if order_dict['Product ID'].startswith('X'):
                    pass
                else:
                    order = pd.Series(order_dict)
                    df = pd.concat([df, order.to_frame().T])
                    print(sku)
                    icount = icount + 1
        df = df.merge(right=pullLocal(), how='left', on='Product ID')
        df.drop('Unit_x', axis=1, inplace=True)
        df.rename(columns={'Unit_y': 'Unit'}, inplace=True)
        print(df)
        df = df[header2]
        shipMapping = {
            'Ground': 'R02R',
            '3 Day Select': 'U21',
            '2nd Day Air PM': 'U07',
            'Next Day Air PM': 'U43',
            'UPS Standard': 'U12',
            'UPS┬« Ground': 'U12',
            'UPS 3 Day Select┬«': 'U21',
            'Free': 'RES',
            'UPS Expedited': 'U12',
            'Priority Mail': 'M02',
            'UPSÂ® Ground': 'U12',
            'Spee-Dee': 'SPD',
            'First-Class Mail Package Service': 'M01',
            'UPS Next Day Air SaverÂ®': 'U43',
            'UPS Next Day AirÂ®': 'U01',
            'UPS 2nd Day AirÂ®': 'U07',
            'UPS Next Day AirÂ® Early': 'U60',
            'Truck': 'TRUCK',
            'UPS Next Day Air SaverÂ®': 'U43',
            'UPS Next Day AirÂ®': 'U01',
            'UPS 2nd Day Air┬«': 'U07',
            'Priority Overnight': 'F01',
            '2nd Day': 'F11',
        }
        df['Shipping Method'] = df['Shipping Method'].replace(shipMapping)
        print(df)
        df.to_csv('test.csv', index=False)




    if response.status_code == 400:
        print(response.content)
    if response.status_code != 200 and response.status_code != 400:
        # print('FFFFFF')
        while response.status_code != 200 and response.status_code != 400:
            print('retrying...')
            time.sleep(10)
            response = session.get(api_url, headers=headers)
            print(response.status_code)