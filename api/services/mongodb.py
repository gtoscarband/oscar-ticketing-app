import imp
import os
from pymongo import MongoClient

def test():
    print("TESTING CONNECTION...")
    uri = os.environ.get("MONGODB_URI")
    client = MongoClient(uri)
    db = client.test
    print(db)