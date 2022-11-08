import pyodbc
import pandas as pd
import pymongo
from dotenv import load_dotenv
import os


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
        # print(conn_str)
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
    qq = orders.find()
    cursor.execute(query)
    # Assigns all remaining rows to a list
    rows = cursor.fetchall()
    print('pulling data...')
    orderMansPants = pd.DataFrame(list(qq))
    localMansPants = pd.read_sql(query, cnxn)
    print('data pulled')
    # Close the connection
    cnxn.close()

    localMansPants.rename(columns={"TransId": "traverse_id", "TrackingNum": "tracking"}, inplace=True)
    localMansPants = localMansPants.astype({'traverse_id': 'float64'})
    megaZord = pd.merge(left=orderMansPants, right=localMansPants, on='traverse_id')
    print(megaZord)
scrape()