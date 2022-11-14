import pymongo
import datetime
import traceback
import time
from dotenv import load_dotenv
import os
import re
import json
global client
global db
global orders



load_dotenv()
dbaddr = os.getenv('DBADDR')
client = pymongo.MongoClient(dbaddr)
db = client["wwmongo"]
orders = db["orders"]


class order:
    def __init__(self, entity_id=None, increment_id=None, traverse_id=None, tracking=None):
        self.entity_id = entity_id
        self.increment_id = increment_id
        self.traverse_id = traverse_id
        self.tracking = tracking
        #print(f'the object has entity_id: {self.entity_id}')

    def __str__(self):
        gen = (str(x) for x in orders.find({"increment_id": self.increment_id}))
        d = ', '.join(map(str, gen))
        return d

    def new(self):
        now = datetime.datetime.utcnow()
        data = {'_id': self.increment_id, 'entity_id': self.entity_id, 'increment_id': self.increment_id,
                'traverse_id': self.traverse_id, 'tracking': self.tracking, 'dateCreated': now, 'dateModified': now,
                'isTracked': False}
        try:
            if orders.find_one({'entity_id': self.entity_id}):
                print('order has already been grabbed')
                pass
            else:
                query = orders.insert_one(data)

                print(f'Pushed order {self.entity_id} to local database with ID {query.inserted_id}')
        except:
            traceback.print_exc()

    def update(self, property, value):
        now = datetime.datetime.utcnow()
        query = {'_id': self.increment_id}
        update = {'$set': {property: value, 'dateModified': now}}
        try:
            orders.update_one(query, update)
            print(f'Updated {property} to {value} on order {self.increment_id}')
        except:
            traceback.print_exc()

    def track(self):
        now = datetime.datetime.utcnow()
        try:

            self.update('isTracked', True)
        except:
            traceback.print_exc()

class imports:
    def __init__(self,
                 Order_Number = None,
                 Order_Date = None,
                 Customer_Firstname = None,
                 Customer_Lastname = None,
                 Customer_Number = None,
                 Address_1 = None,
                 Address_2 = None,
                 City = None,
                 State = None,
                 Zip = None,
                 Province_Other = None,
                 Country = None,
                 Home_Phone = None,
                 Work_Phone = None,
                 Work_Ext = None,
                 Email = None,
                 Ship_Name  = None,
                 Ship_Address_1 = None,
                 Ship_Address_2 = None,
                 Ship_City = None,
                 Ship_State = None,
                 Ship_Province_Other = None,
                 Ship_Country = None,
                 Ship_Phone = None,
                 Product_ID = None,
                 Quantity = None,
                 Unit_Price = None,
                 Unit = None,
                 Cut_List = None,
                 Cut_Charge = None,
                 Shipping_Cost = None,
                 Tax_Rate = None,
                 Promotion_Code = None,
                 Discount = None,
                 Shipping_Method = None,
                 Payment_Type = None,
                 Comments = None,
                 Company = None,
                 RepId = None,
                 ShipAtt = None,
                 ):
        self.Order_Number = Order_Number
        self.Order_Date = Order_Date
        self.Customer_Firstname = Customer_Firstname
        self.Customer_Lastname = Customer_Lastname
        self.Customer_Number = Customer_Number
        self.Address_1 = Address_1
        self.Address_2 = Address_2
        self.City = City
        self.State = State
        self.Zip = Zip
        self.Province_Other = Province_Other
        self.Country = Country
        self.Home_Phone = Home_Phone
        self.Work_Phone = Work_Phone
        self.Work_Ext = Work_Ext
        self.Email = Email
        self.Ship_Name = Ship_Name
        self.Ship_Address_1 = Ship_Address_1
        self.Ship_Address_2 = Ship_Address_2
        self.Ship_City = Ship_City
        self.Ship_State = Ship_State
        self.Ship_Province_Other = Ship_Province_Other
        self.Ship_Country = Ship_Country
        self.Ship_Phone = Ship_Phone
        self.Product_ID = Product_ID
        self.Quantity = Quantity
        self.Unit_Price = Unit_Price
        self.Unit = Unit
        self.Cut_List = Cut_List
        self.Cut_Charge = Cut_Charge
        self.Shipping_Cost = Shipping_Cost
        self.Tax_Rate = Tax_Rate
        self.Promotion_Code = Promotion_Code
        self.Discount = Discount
        self.Shipping_Method = Shipping_Method
        self.Payment_Type = Payment_Type
        self.Comments = Comments
        self.Company = Company
        self.RepId = RepId
        self.ShipAtt = ShipAtt
        #print(f'the object has entity_id: {self.entity_id}')

    def __str__(self):
        '''gen = (str(x) for x in orders.find({"increment_id": self.increment_id}))
        d = ', '.join(map(str, gen))'''
        return self

    def imports(self):
        print(self)
        '''load_dotenv()
        dbaddr = os.getenv('DBADDR')
        client = pymongo.MongoClient(dbaddr)
        db = client["wwmongo"]
        imports = db["imports"]'''