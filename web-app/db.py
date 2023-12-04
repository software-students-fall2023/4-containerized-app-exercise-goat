"""import pymongo"""
from pymongo.mongo_client import MongoClient

client = MongoClient("mongodb://db:27017")
db = client["project4"]
collection = db["savehere"]


def get_most_recent_transcript():
    """fetch the most recent transcript from the database"""
    try:
        documents_with_time = collection.find({"time": {"$exists": True}})
        most_recent_document = max(documents_with_time, key=lambda x: x["time"])
        return most_recent_document["transcript"]
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error: {e}")
        return None
