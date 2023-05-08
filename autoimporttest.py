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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

thread_local = local()

token = os.getenv('BEARER')
headers = {'Authorization': f'Bearer {token}'}
headers2 = {'Authorization': f'Bearer {token}', 'Accept': 'application/pdf'}
now = str(datetime.datetime.utcnow())

def alpha2_to_alpha3(alpha2_code):
    country_codes = {
        'AD': 'AND', 'AE': 'ARE', 'AF': 'AFG', 'AG': 'ATG', 'AI': 'AIA', 'AL': 'ALB', 'AM': 'ARM',
        'AO': 'AGO', 'AQ': 'ATA', 'AR': 'ARG', 'AS': 'ASM', 'AT': 'AUT', 'AU': 'AUS', 'AW': 'ABW',
        'AX': 'ALA', 'AZ': 'AZE', 'BA': 'BIH', 'BB': 'BRB', 'BD': 'BGD', 'BE': 'BEL', 'BF': 'BFA',
        'BG': 'BGR', 'BH': 'BHR', 'BI': 'BDI', 'BJ': 'BEN', 'BL': 'BLM', 'BM': 'BMU', 'BN': 'BRN',
        'BO': 'BOL', 'BQ': 'BES', 'BR': 'BRA', 'BS': 'BHS', 'BT': 'BTN', 'BV': 'BVT', 'BW': 'BWA',
        'BY': 'BLR', 'BZ': 'BLZ', 'CA': 'CAN', 'CC': 'CCK', 'CD': 'COD', 'CF': 'CAF', 'CG': 'COG',
        'CH': 'CHE', 'CI': 'CIV', 'CK': 'COK', 'CL': 'CHL', 'CM': 'CMR', 'CN': 'CHN', 'CO': 'COL',
        'CR': 'CRI', 'CU': 'CUB', 'CV': 'CPV', 'CW': 'CUW', 'CX': 'CXR', 'CY': 'CYP', 'CZ': 'CZE',
        'DE': 'DEU', 'DJ': 'DJI', 'DK': 'DNK', 'DM': 'DMA', 'DO': 'DOM', 'DZ': 'DZA', 'EC': 'ECU',
        'EE': 'EST', 'EG': 'EGY', 'EH': 'ESH', 'ER': 'ERI', 'ES': 'ESP', 'ET': 'ETH', 'FI': 'FIN',
        'FJ': 'FJI', 'FK': 'FLK', 'FM': 'FSM', 'FO': 'FRO', 'FR': 'FRA', 'GA': 'GAB', 'GB': 'GBR',
        'GD': 'GRD', 'GE': 'GEO', 'GF': 'GUF', 'GG': 'GGY', 'GH': 'GHA', 'GI': 'GIB', 'GL': 'GRL',
        'GM': 'GMB', 'GN': 'GIN', 'GP': 'GLP', 'GQ': 'GNQ', 'GR': 'GRC', 'GS': 'SGS', 'GT': 'GTM',
        'GU': 'GUM', 'GW': 'GNB', 'GY': 'GUY', 'HK': 'HKG', 'HM': 'HMD', 'HN': 'HND', 'HR': 'HRV',
        'HT': 'HTI', 'HU': 'HUN', 'ID': 'IDN', 'IE': 'IRL', 'IL': 'ISR', 'IM': 'IMN', 'IN': 'IND',
        'IO': 'IOT', 'IQ': 'IRQ', 'IR': 'IRN', 'IS': 'ISL', 'IT': 'ITA', 'JE': 'JEY', 'JM': 'JAM',
        'JO': 'JOR', 'JP': 'JPN', 'KE': 'KEN', 'KG': 'KGZ', 'KH': 'KHM', 'KI': 'KIR', 'KM': 'COM',
        'KN': 'KNA', 'KP': 'PRK', 'KR': 'KOR', 'KW': 'KWT', 'KY': 'CYM', 'KZ': 'KAZ', 'LA': 'LAO',
        'LB': 'LBN', 'LC': 'LCA', 'LI': 'LIE', 'LK': 'LKA', 'LR': 'LBR', 'LS': 'LSO', 'LT': 'LTU',
        'LU': 'LUX', 'LV': 'LVA', 'LY': 'LBY', 'MA': 'MAR', 'MC': 'MCO', 'MD': 'MDA', 'ME': 'MNE',
        'MF': 'MAF', 'MG': 'MDG', 'MH': 'MHL', 'MK': 'MKD', 'ML': 'MLI', 'MM': 'MMR', 'MN': 'MNG',
        'MO': 'MAC', 'MP': 'MNP', 'MQ': 'MTQ', 'MR': 'MRT', 'MS': 'MSR', 'MT': 'MLT', 'MU': 'MUS',
        'MV': 'MDV', 'MW': 'MWI', 'MX': 'MEX', 'MY': 'MYS', 'MZ': 'MOZ', 'NA': 'NAM', 'NC': 'NCL',
        'NE': 'NER', 'NF': 'NFK', 'NG': 'NGA', 'NI': 'NIC', 'NL': 'NLD', 'NO': 'NOR', 'NP': 'NPL',
        'NR': 'NRU', 'NU': 'NIU', 'NZ': 'NZL', 'OM': 'OMN', 'PA': 'PAN', 'PE': 'PER', 'PF': 'PYF',
        'PG': 'PNG', 'PH': 'PHL', 'PK': 'PAK', 'PL': 'POL', 'PM': 'SPM', 'PN': 'PCN', 'PR': 'PRI',
        'PS': 'PSE', 'PT': 'PRT', 'PW': 'PLW', 'PY': 'PRY', 'QA': 'QAT', 'RE': 'REU', 'RO': 'ROU',
        'RS': 'SRB', 'RU': 'RUS', 'RW': 'RWA', 'SA': 'SAU', 'SB': 'SLB', 'SC': 'SYC', 'SD': 'SDN',
        'SE': 'SWE', 'SG': 'SGP', 'SH': 'SHN', 'SI': 'SVN', 'SJ': 'SJM', 'SK': 'SVK', 'SL': 'SLE',
        'SM': 'SMR', 'SN': 'SEN', 'SO': 'SOM', 'SR': 'SUR', 'SS': 'SSD', 'ST': 'STP', 'SV': 'SLV',
        'SX': 'SXM', 'SY': 'SYR', 'SZ': 'SWZ', 'TC': 'TCA', 'TD': 'TCD', 'TF': 'ATF', 'TG': 'TGO',
        'TH': 'THA', 'TJ': 'TJK', 'TK': 'TKL', 'TL': 'TLS', 'TM': 'TKM', 'TN': 'TUN', 'TO': 'TON',
        'TR': 'TUR', 'TT': 'TTO', 'TV': 'TUV', 'TW': 'TWN', 'TZ': 'TZA', 'UA': 'UKR', 'UG': 'UGA',
        'UM': 'UMI','US': 'USA', 'UY': 'URY', 'UZ': 'UZB', 'VA': 'VAT', 'VC': 'VCT', 'VE': 'VEN',
        'VG': 'VGB', 'VI': 'VIR', 'VN': 'VNM', 'VU': 'VUT', 'WF': 'WLF', 'WS': 'WSM', 'YE': 'YEM',
        'YT': 'MYT','ZA': 'ZAF', 'ZM': 'ZMB', 'ZW': 'ZWE'}

    alpha3_code = country_codes.get(alpha2_code.upper(), None)

    if alpha3_code is None:
        raise ValueError(f"Invalid Alpha-2 country code: {alpha2_code}")

    return alpha3_code




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
entdf = pd.DataFrame(columns=['entity', 'order number'])
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
            entity_id = y['entity_id']
            this_order_number = y['increment_id']
            entd = {'entity': entity_id, 'order number': this_order_number}
            ents = pd.Series(entd)
            entdf = pd.concat([entdf, ents.to_frame().T])
            this_order_date = y['created_at']
            cfname = y['billing_address']['firstname']
            clname = y['billing_address']['lastname']
            att = cfname + ' ' + clname
            baddone = y['billing_address']['street'][0]
            if len(y['billing_address']['street']) > 1:
                baddtwo = y['billing_address']['street'][1]
            else:
                baddtwo = None
            ccity = y['billing_address']['city']
            cstate = y['billing_address']['region_code']
            czip = y['billing_address']['postcode']
            ccountry_code = alpha2_to_alpha3(y['billing_address']['country_id'])
            if 'company' in y['billing_address'].keys():
                company = y['billing_address']['company']
            else:
                company = None
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
            sstate = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['region_code']
            szip = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['postcode']
            scountry_code = alpha2_to_alpha3(y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['country_id'])
            sphone = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['telephone']
            real_shipping = y['shipping_invoiced']
            shipping = 0
            payment_type = y['payment']['method']
            ship_method = y['shipping_description']
            #co_name = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['company']
            icount = 0
            real_tax_rate = y['base_tax_invoiced']
            for i in y['items']:
                sku = i['sku']
                qty = i['qty_ordered']
                price = i['base_price']
                unit = None
                tax_rate = 0
                promo_code = None
                discount = i['discount_invoiced']
                comments = None

                cut_list = None
                cut_charge = None
                if ccountry_code == 'USA':
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
                        'Company': company,
                        'ShipAtt': att
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
                        'Company': company,
                        'ShipAtt': att
                    }
                if icount == 0:
                    order_dict['Tax Rate'] = real_tax_rate
                    order_dict['Shipping Cost'] = real_shipping
                    icount = icount + 1

                if order_dict['Product ID'].startswith('X'):
                    bundle = order_dict['Product ID'].split('-')
                    for x in bundle:
                        print(x)
                order = pd.Series(order_dict)
                df = pd.concat([df, order.to_frame().T])


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
            'UPS 3 Day Select®': 'U21',
            'Free': 'RES',
            'UPS Expedited': 'U12',
            'Priority Mail': 'M02',
            'UPS® Ground': 'U12',
            'Spee-Dee': 'SPD',
            'First-Class Mail Package Service': 'M01',
            'UPS Next Day Air Saver®': 'U43',
            'UPS Next Day Air®': 'U01',
            'UPS 2nd Day Air®': 'U07',
            'UPS Next Day Air® Early': 'U60',
            'Truck': 'TRUCK',
            'UPS Next Day Air Saver®': 'U43',
            'UPS Next Day Air®': 'U01',
            'UPS 2nd Day Air®': 'U07',
            'Priority Overnight': 'F01',
            '2nd Day': 'F11',
        }
        df['Shipping Method'] = df['Shipping Method'].replace(shipMapping)
        print(df)
        filename = 'WWAutoOrderImport' + ' ' + now + '.csv'
        filepath = '/home/ftp/WWtrackingImport/pdfs'
        fullfile = os.path.join(filepath, filename)
        df.to_csv(fullfile, index=False)




    if response.status_code == 400:
        print(response.content)
    if response.status_code != 200 and response.status_code != 400:
        # print('FFFFFF')
        while response.status_code != 200 and response.status_code != 400:
            print('retrying...')
            time.sleep(10)
            response = session.get(api_url_proc, headers=headers)
            print(response.status_code)




from_email = "sales@hdlusa.com"
from_password = os.getenv('EMAIL_CRED')
to_emails = ["tbarker@hdlusa.com"]

# Create the message
subject = f"[AUTOMATIC] WW Order Import {now}"



port = 465


body = "Hello, please find the attached file for the WW Order Import."


# Attachment
attachment_path = fullfile  # Provide the path to your attachment




# Create a MIMEMultipart message
msg = MIMEMultipart()
msg["From"] = from_email
msg["To"] = ", ".join(to_emails)
msg["Subject"] = subject

# Attach the email body
msg.attach(MIMEText(body, "plain"))

# Attach the file
with open(attachment_path, "rb") as f:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {os.path.basename(attachment_path)}",
    )
    msg.attach(part)

# Connect to the SMTP server and send the email
try:
    server = smtplib.SMTP_SSL("mail.runspot.net", 465)
    server.login(from_email, from_password)
    server.sendmail(from_email, to_emails, msg.as_string())
    server.quit()
    print("Email with attachment sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
