#testing pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.testdb

coll = db.testcoll

test = coll.insert_one(
{"name":'Daniel'}
)

cursor = coll.find({"name": "Daniel"})

for document in cursor:
    print document
