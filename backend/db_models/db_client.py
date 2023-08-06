from pymongo import MongoClient
import os

def get_mongo_db():
    mongo_client = MongoClient(os.environ["MONGODB_URL"])
    return mongo_client