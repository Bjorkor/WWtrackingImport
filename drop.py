from dotenv import load_dotenv
import pymongo
import os
load_dotenv()
dbaddr = os.getenv('DBADDR')
client = pymongo.MongoClient(dbaddr)
db = client["wwmongo"]
orders = db["orders"]
q = { 'isTracked': True }
x = orders.delete_many(q)

print(x.deleted_count, " documents deleted.")
