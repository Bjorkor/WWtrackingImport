
import pandas as pd
import pymongo
from dotenv import load_dotenv
import os
import datetime
from orderMan import order

#local = pd.read_csv('local.csv')
#order = pd.read_csv('order.csv')
load_dotenv()
dbaddr = os.getenv('DBADDR')
client = pymongo.MongoClient(dbaddr)
db = client["wwmongo"]
orders = db["orders"]
def work(local, order):
    local['tracking'] = local[local['tracking'].astype('string')]
    print('local')
    print(local.dtypes)
    print(local)
    print('order')
    print(order.dtypes)
    print(order)
print('i am doing thingsssssss')
nums = [999999, 999999, 999999, 300574]
for x in nums:
    print(x)
    for y in orders.find({'entity_id': x}):
        if order(y):
            print(y)
            print('pog')
        else:
            print('antipog')

