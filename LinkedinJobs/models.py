import re
from pymongo import MongoClient
from config import Config


class MongoDBUtility:
    def __init__(self, uri, db_name, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_data(self, data):
        for item in data:
            # Extract the numeric ID from the trackingUrn
            match = re.search(r"\d+", item.get("trackingUrn", ""))
            numeric_id = match.group(0) if match else None

            # Construct the LinkedIn URL using the numeric ID
            linkedin_url = (
                f"https://www.linkedin.com/jobs/view/{numeric_id}"
                if numeric_id
                else None
            )

            # Extract location information
            location = item.get("secondaryDescription", {}).get(
                "text", "Location Not Available"
            )

            # Update the MongoDB document with the LinkedIn URL if it doesn't exist
            update_doc = {
                "$setOnInsert": item,
            }
            if linkedin_url:
                update_doc["$set"] = {"linkedinURL": linkedin_url}

            self.collection.update_one(
                {"trackingUrn": item["trackingUrn"]}, update_doc, upsert=True
            )
