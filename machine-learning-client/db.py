"""use pymongo database"""
from datetime import datetime
from pymongo.mongo_client import MongoClient


client = MongoClient("mongodb://db:27017")
db = client["project4"]
collection = db["savehere"]


def save_transcript(transcript, name, path="curr.wav"):
    """save transcript and audio raw data to database"""
    with open(path, "rb") as file:
        file_data = file.read()
        file_document = {
            "time": datetime.now(),
            "data": file_data,
            "transcript": transcript,
            "name": name,
        }
        result = collection.insert_one(file_document)
        print(f"WAV file inserted with _id: {result.inserted_id}")
