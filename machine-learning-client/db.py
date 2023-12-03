from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import os
client = MongoClient('localhost', 27017)
db = client['project4']
collection = db['savehere']
def save_transcript(transcript,name,path='curr.wav'):
    with open(path, 'rb') as file:
        file_data = file.read()
        file_document={
            'time':datetime.now(),
            'data': file_data,
            'transcript':transcript,
            'name': name,
        }
        result = collection.insert_one(file_document)
        print(f"WAV file inserted with _id: {result.inserted_id}")

def get_most_recent_audio(Id):
    try:
        documents_with_time = collection.find({'id':Id, 'time': {'$exists': True}})

        if documents_with_time.count() == 0:
            return None  
        most_recent_document = max(documents_with_time, key=lambda x: x['time'])
        return most_recent_document
    except Exception as e:
        print(f"Error: {e}")
        return None

