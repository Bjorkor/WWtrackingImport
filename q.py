from dotenv import load_dotenv
import pymongo
import os
import datetime
load_dotenv()
dbaddr = os.getenv('DBADDR')
client = pymongo.MongoClient(dbaddr)
db = client["wwmongo"]
orders = db["orders"]
myquery = { "isTracked": False }
for x in orders.find(myquery):
    print(x)
