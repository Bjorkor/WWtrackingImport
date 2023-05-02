from dotenv import load_dotenv
import pymongo
import os
load_dotenv()
dbaddr = os.getenv('DBADDR')
client = pymongo.MongoClient(dbaddr)
db = client["wwmongo"]
orders = db["orders"]
q = { 'isTracked': True }
for x in orders.find(q):
    print(x)
