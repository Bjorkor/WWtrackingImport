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
    #localMansPants['increment_id'] = localMansPants['increment_id'].convert_dtypes().astype('int', errors='ignore').convert_dtypes()
    #localMansPants['increment_id'] = localMansPants['increment_id'].convert_dtypes().astype('int', errors='ignore').convert_dtypes()
    #localMansPants[["increment_id"]] = localMansPants[["increment_id"]].apply(pd.to_numeric, errors='ignore')
    #localMansPants['tracking'] = localMansPants['tracking'].convert_dtypes().astype('str', errors='ignore').convert_dtypes()
    #localMansPants['traverse_id'] = localMansPants['traverse_id'].convert_dtypes().astype('str', errors='ignore').convert_dtypes()
    #orderMansPants['increment_id'] = orderMansPants['increment_id'].convert_dtypes().astype('int', errors='ignore').convert_dtypes()
    #localMansPants = localMansPants[isinstance(localMansPants['increment_id'], int)]
    #localMansPants2 = localMansPants.apply(lambda x: x.astype('object'))
    #orderMansPants2 = orderMansPants.apply(lambda x: x.astype('object'))
    #localMansPants = localMansPants.infer_objects()#localMansPants.astype({'increment_id': int}, errors='ignore')
    #megaZord = pd.concat([orderMansPants2, localMansPants2], ignore_index=True, axis=0, join='inner')
    #print(localMansPants.astype({'increment_id': 'int'}, errors='ignore').dtypes)
    #megaZord = pd.merge(left=orderMansPants, right=localMansPants, how='left', on='increment_id')
    #print(megaZord)
    localMansPants.dropna(inplace=True)
    localMansPants = localMansPants[localMansPants['increment_id'].apply(lambda x: len(x) == 10)]
    localMansPants = localMansPants[localMansPants['traverse_id'].apply(lambda x: str(x).startswith('2'))]
    localMansPants[["increment_id"]] = localMansPants[["increment_id"]].apply(pd.to_numeric, errors='ignore')
    localMansPants['traverse_id'] = localMansPants[localMansPants['traverse_id'].astype(int)]
    localMansPants['tracking'] = localMansPants[localMansPants['tracking'].convert_dtypes().astype(str)]
    megaZord = pd.merge(left=orderMansPants, right=localMansPants, how='left', on='increment_id')
    #localMansPantsfloat = localMansPants.select_dtypes(include='float64')
    #localMansPantsint = localMansPants.select_dtypes(include='int64')
    #print(localMansPantsfloat.dtypes)
    #print(localMansPantsfloat)
    #print(localMansPantsint.dtypes)
    #print(localMansPantsint)
    print(localMansPants)
    localMansPants.to_csv('localpants.csv')
    print(localMansPants.dtypes)
    print(orderMansPants.dtypes)
    print(megaZord)
    #print(orderMansPants2.astype({'increment_id': 'int'}, errors='ignore').dtypes)
scrape()