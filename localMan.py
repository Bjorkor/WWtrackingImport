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
    qq = orders.find({'isTracked': False})
    cursor.execute(query)
    # Assigns all remaining rows to a list
    rows = cursor.fetchall()
    print('pulling data...')
    orderMansPants = pd.DataFrame(list(qq))
    localMansPants = pd.read_sql(query, cnxn)
    print('data pulled')
    # Close the connection
    cnxn.close()

    localMansPants.rename(columns={"TransId": "traverse_id", "TrackingNum": "tracking", "cf_External Trans Id": "increment_id"}, inplace=True)

    orderMansPants = orderMansPants[['entity_id', 'increment_id', 'dateCreated', 'dateModified', 'isTracked']]
    localMansPants = localMansPants.dropna()
    localMansPants = localMansPants[localMansPants['increment_id'].apply(lambda x: len(x) == 10)]
    megazord = pd.merge(left=orderMansPants, right=localMansPants, on='increment_id', how='left')
    print(megazord)
scrape()
