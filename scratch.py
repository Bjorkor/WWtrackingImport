import pymongo
import datetime
import traceback
now = datetime.datetime.utcnow()
client = pymongo.MongoClient("mongodb://172.29.15.43:9000/")
db = client["wwmongo"]
orders = db["orders"]


"""x = orders.insert_one(data)
query = {}

result = orders.find(query)

for y in result:
    print(y)"""
client = pymongo.MongoClient("mongodb://172.29.15.43:9000/")
db = client["wwmongo"]
orders = db["orders"]
try:
    for x in orders.find():
        print(x)

except:
    traceback.print_exc()

