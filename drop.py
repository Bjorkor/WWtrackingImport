from dotenv import load_dotenv
import pymongo
import os
import datetime
load_dotenv()
dbaddr = os.getenv('DBADDR')
client = pymongo.MongoClient(dbaddr)
db = client["wwmongo"]
orders = db["orders"]


d = datetime.datetime(2023, 4, 28, 21, 46, 8, 597000)
q = { "isTracked": False }
x = orders.delete_many(q)

print(x.deleted_count, " documents deleted.")
