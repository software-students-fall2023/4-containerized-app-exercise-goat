from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

client = MongoClient("mongodb://db:27017")
db = client['project4']
collection = db['savehere']
def get_most_recent_transcript():
    try:
        documents_with_time = collection.find({'time': {'$exists': True}})
        most_recent_document = max(documents_with_time, key=lambda x: x['time'])
        return most_recent_document['transcript']
    except Exception as e:
        print(f"Error: {e}")
        return None