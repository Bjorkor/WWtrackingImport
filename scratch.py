
import pandas as pd
import pymongo
from dotenv import load_dotenv
import os
import datetime

local = pd.read_csv('local.csv')
order = pd.read_csv('order.csv')

def work(local, order):
    local['tracking'] = local[local['tracking'].astype('string')]
    print('local')
    print(local.dtypes)
    print(local)
    print('order')
    print(order.dtypes)
    print(order)


work(local, order)


