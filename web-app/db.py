from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

uri = "mongodb+srv://2SEProjectDatabase:ThisIsThePassword123@cluster0.21yazmx.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, tlsAllowInvalidCertificates=True, server_api=ServerApi('1'))
databaseclient = client["account"]
database = databaseclient['account']
collection = databaseclient["Username+Password"]
def get_most_recent_transcript():
    try:
        documents_with_time = collection.find({'time': {'$exists': True}})
        most_recent_document = max(documents_with_time, key=lambda x: x['time'])
        return most_recent_document['transcript']
    except Exception as e:
        print(f"Error: {e}")
        return None