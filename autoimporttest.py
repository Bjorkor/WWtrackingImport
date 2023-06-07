import sqlite3 as sl
import requests
from requests.sessions import Session
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, local
import time
import datetime
from dotenv import load_dotenv
import os
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

# set some variables
thread_local = local()
token = os.getenv('BEARER')
headers = {'Authorization': f'Bearer {token}'}
now = str(datetime.datetime.utcnow())


# functions

def recallLastOrder():
    try:
        with open('lastorder', 'w') as f:
            content = f.read()
        return int(content)
    except:
        return 0


def saveLastOrder(string):
    with open('lastorder', 'w') as f:
        f.write(string)


def get_zip_info(zip_code):
    base_url = "https://www.zipcodeapi.com/rest/FokPyKZbaIf0lAHFjfGe3X5NkiGNfuZey430khU3HldnvthYpUGfbbpz30xE3udl/info.json"
    url = f"{base_url}/{zip_code}/degrees"

    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.content)['state']
    else:
        return None


def alpha2_to_alpha3(alpha2_code):
    # convert 2 char country codes to 3 char country codes
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
        'UM': 'UMI', 'US': 'USA', 'UY': 'URY', 'UZ': 'UZB', 'VA': 'VAT', 'VC': 'VCT', 'VE': 'VEN',
        'VG': 'VGB', 'VI': 'VIR', 'VN': 'VNM', 'VU': 'VUT', 'WF': 'WLF', 'WS': 'WSM', 'YE': 'YEM',
        'YT': 'MYT', 'ZA': 'ZAF', 'ZM': 'ZMB', 'ZW': 'ZWE'}

    alpha3_code = country_codes.get(alpha2_code.upper(), None)

    if alpha3_code is None:
        raise ValueError(f"Invalid Alpha-2 country code: {alpha2_code}")

    return alpha3_code


def get_session() -> Session:
    # use the current web session
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session


def pullLocal():
    # query local database, returns pandas dataframe with SKU and Unit of Measure
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


# main start


# load variables from .env file
load_dotenv()

# connect to local mongodb instance
dbaddr = os.getenv('DBADDR')
client = pymongo.MongoClient(dbaddr)
db = client["wwmongo"]

# Define final column titles
header2 = ["Order Number", "Order Date", "Customer Firstname", "Customer Lastname", "Customer Number", "Address 1",
           "Address 2", "City", "State", "Zip", "Province/Other", "Country", "Home Phone", "Work Phone", "Work Ext",
           "Email", "Ship Name", "Ship Address 1", "Ship Address 2", "Ship City", "Ship State", "Ship Zip",
           "Ship Province/Other", "Ship Country", "Ship Phone", "Product ID", "Quantity", "Unit Price", "Unit",
           "Cut List", "Cut Charge", "Shipping Cost", "Tax Rate", "Promotion Code", "Discount", "Shipping Method",
           "Payment Type", "Comments", "Company", "RepId", "ShipAtt"]

# Create empty dataframe using above headers
df = pd.DataFrame(columns=header2)

# Create empty dataframe using entity and order number as headings
entdf = pd.DataFrame(columns=['entity', 'order number'])

# no idea what's happening here
# units = pullLocal()

# get the current web session and set it to session variable
session = get_session()

# open connection using session
with session as session:
    # url for magento api orders endpoint
    api_url_proc = 'https://wwhardware.com/rest/default/V1/orders?searchCriteria[pageSize]=1000&searchCriteria[filterGroups][0][filters][0][field]=status&searchCriteria[filterGroups][0][filters][0][value]=processing'

    # send a GET request to api_url_proc using secure headers
    response = session.get(api_url_proc, headers=headers)

    # if response is GOOD, do stuff
    if response.status_code == 200:
        # set content of response to a variable
        yres = json.loads(response.content)

        # for each ORDER in the batch
        for y in yres['items']:
            print(y['increment_id'])
            # set variables

            # hidden magento order ID
            entity_id = y['entity_id']

            # public magento order ID
            this_order_number = y['increment_id']

            # what?
            """entd = {'entity': entity_id, 'order number': this_order_number}
            ents = pd.Series(entd)
            entdf = pd.concat([entdf, ents.to_frame().T])"""

            # magento's reported order date
            this_order_date = y['created_at']

            # billing first and last name
            cfname = y['billing_address']['firstname']
            clname = y['billing_address']['lastname']

            # attention field is first name + last name
            att = cfname + ' ' + clname

            # billing address line one
            baddone = y['billing_address']['street'][0]

            # check if billing address has more than one line
            if len(y['billing_address']['street']) > 1:
                # if yes, set line 2 to a variable
                baddtwo = y['billing_address']['street'][1]
            else:
                # if no, set variable to None
                baddtwo = None

            # billing address city
            ccity = y['billing_address']['city']

            # billing address region code (state, province)
            if 'region_code' in y['billing_address'].keys():
                print('billing region code found')
                cstate = y['billing_address']['region_code']
            else:
                print('billing region code NOT found')
                cstate = None

            # billing zip code
            czip = y['billing_address']['postcode']

            # billing country code, converted from 2 chars to 3 chars
            ccountry_code = alpha2_to_alpha3(y['billing_address']['country_id'])

            # check if a company name has been provided by the customer
            if 'company' in y['billing_address'].keys():
                # if yes, set that to a variable
                company = y['billing_address']['company']
            else:
                # if no, set variable to None
                company = None

            # billing address phone number
            hphone = y['billing_address']['telephone']

            # billing address email
            this_email = y['billing_address']['email']

            # shipping first name
            sfname = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['firstname']

            # shipping last name
            slname = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['lastname']

            # shipping address line one
            saddone = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['street'][0]

            # check if shipping address has more than one line
            if len(y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['street']) > 1:
                # if yes set it to a variable
                saddtwo = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['street'][1]
            else:
                # if no, set variable to None
                saddtwo = None

            # shipping address city
            scity = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['city']

            # shipping address region code (state, province)
            if 'region_code' in y['extension_attributes']['shipping_assignments'][0]['shipping']['address'].keys():

                sstate = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['region_code']
                print(f'shipping region code found: {sstate}')
            else:
                print('shipping region code NOT found')
                q = str(y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['postcode'])[:5]
                z = get_zip_info(q)
                print(q)
                sstate = z

            # shipping address zip code
            szip = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['postcode']

            # shipping address country code, converted from 2 chars to 3 chars
            scountry_code = alpha2_to_alpha3(
                y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['country_id'])

            # shipping address phone number
            sphone = y['extension_attributes']['shipping_assignments'][0]['shipping']['address']['telephone']

            # actual shipping charged to the customer
            real_shipping = y['shipping_invoiced']

            # placeholder shippng charge value for the purpose of formatting the final output
            shipping = 0

            # payment method
            payment_type = y['payment']['method']

            # shipping method
            ship_method = y['shipping_description']

            # item count
            icount = 0

            # actual tax charged to customer
            real_tax_rate = y['base_tax_invoiced']

            # for each ITEM in the ORDER
            for i in y['items']:

                # product ordered
                sku = i['sku']

                # quantity ordered
                qty = i['qty_ordered']

                # price of the product
                price = i['base_price']

                # product unit of measure, to be populated later
                unit = None

                # placeholder tax rate value for the purpose of formatting the final output
                tax_rate = 0

                # promo code placeholder
                promo_code = None

                # discount amount
                discount = i['discount_invoiced']

                # comments placeholder
                comments = None

                # list of cuts to make for long/irregular products
                cut_list = None

                # charge associated with above cuttings
                cut_charge = None

                # check if the order is going to the USA
                if ccountry_code == 'USA':
                    # if yes, use this version of the dictionary, suited to orders going to the united states
                    # 'Ship Province/Other' & 'Province/Other' are set to None, and the region codes are mapped to the 'State' fields
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
                    # if no, use this version of the dictionary, suited for international orders
                    # 'State' & 'Ship State' are set to None, and the region codes are mapped to the 'Province/Other' fields
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
                        'Ship State': sstate,
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

                # check if the item is a bundle part number
                if order_dict['Product ID'].startswith('X'):
                    # end this iteration
                    continue

                # check if the item count is zero
                if icount == 0:
                    # if yes, set the tax and shipping rate fields to their real values, and increment the item count by 1
                    order_dict['Tax Rate'] = real_tax_rate
                    order_dict['Shipping Cost'] = real_shipping
                    icount = icount + 1

                # set the now populated dictionary to a pandas series
                order = pd.Series(order_dict)

                # add the series created above to the blank dataframe created at the beginning of the script
                df = pd.concat([df, order.to_frame().T])

        # merge orders dataframe with the unit of measure dataframe from pullLocal(), using part number as the key
        df = df.merge(right=pullLocal(), how='left', on='Product ID')

        # drop extra column
        df.drop('Unit_x', axis=1, inplace=True)

        # rename unit of measure column
        df.rename(columns={'Unit_y': 'Unit'}, inplace=True)

        # set dataframe headers to those specified by the header list
        df = df[header2]

        # dictionary for mapping magento ship methods to traverse ship via codes
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

        # replace magento ship methods using above mapping
        df['Shipping Method'] = df['Shipping Method'].replace(shipMapping)

        # set name and path of output file using datetime at runtime
        filename = 'WWAutoOrderImport' + ' ' + now + '.csv'
        filepath = '/home/ftp/WWtrackingImport/pdfs'
        fullfile = os.path.join(filepath, filename)

        df['Order Number'] = df['Order Number'].astype(int)
        df = df[df['Order Number'] > recallLastOrder()]

        saveLastOrder(str(df.iloc[-1]['Order Number']))

        # write final output to csv
        df.to_csv(fullfile, index=False)

    # if response is BAD, print why
    if response.status_code == 400:
        print(response.content)

    # if response is inconclusive, retry
    if response.status_code != 200 and response.status_code != 400:
        # print('FFFFFF')
        while response.status_code != 200 and response.status_code != 400:
            print('retrying...')
            time.sleep(10)
            response = session.get(api_url_proc, headers=headers)
            print(response.status_code)

# setup email message

from_email = "sales@hdlusa.com"
from_password = os.getenv('EMAIL_CRED')
to_emails = ["tbarker@hdlusa.com"]

# Create the message
subject = f"[AUTOMATIC] WW Order Import {now}"

port = 465

body = "Hello, please find the attached file for the WW Order Import."

# Attachment
attachment_path = fullfile

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
