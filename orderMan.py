import pymongo
import datetime
import traceback
import time
from dotenv import load_dotenv
import os

global client
global db
global orders



load_dotenv()
dbaddr = os.getenv('DBADDR')
client = pymongo.MongoClient(dbaddr)
db = client["wwmongo"]
orders = db["orders"]


class order:
    def __init__(self, entity_id, increment_id=None, traverse_id=None, tracking=None):
        self.entity_id = entity_id
        self.increment_id = increment_id
        self.traverse_id = traverse_id
        self.tracking = tracking
        #print(f'the object has entity_id: {self.entity_id}')

    def __str__(self):
        gen = (str(x) for x in orders.find({"entity_id": self.entity_id}))
        d = ', '.join(map(str, gen))
        return d

    def new(self):
        now = datetime.datetime.utcnow()
        data = {'_id': self.entity_id, 'entity_id': self.entity_id, 'increment_id': self.increment_id,
                'traverse_id': self.traverse_id, 'tracking': self.tracking, 'dateCreated': now, 'dateModified': now,
                'isTracked': False}
        try:
            if orders.find_one({'entity_id': self.entity_id}):
                pass
            else:
                query = orders.insert_one(data)

                print(f'Pushed order {self.entity_id} to local database with ID {query.inserted_id}')
        except:
            traceback.print_exc()

    def update(self, property, value):
        now = datetime.datetime.utcnow()
        query = {'_id': self.entity_id}
        update = {'$set': {property: value, 'dateModified': now}}
        try:
            orders.update_one(query, update)
            print(f'Updated {property} to {value} on order {self.entity_id}')
        except:
            traceback.print_exc()

    def track(self):
        now = datetime.datetime.utcnow()
        try:

            self.update('isTracked', True)
        except:
            traceback.print_exc()
