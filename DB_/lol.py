import random
import pymongo
from datetime import datetime, timedelta

# ✅ Connect to MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "SmartCoolingSystem"
COLLECTION_NAME = "Processed_AI_Responses"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# ✅ Define the time range
start_time = datetime(2025, 2, 8, 23, 0, 0)  # Feb 8, 2025, 23:00
end_time = datetime(2025, 2, 9, 14, 0, 0)    # Feb 9, 2025, 14:00

# ✅ Fetch all records from the collection
documents = list(collection.find())

if not documents:
    print("No records found in the database.")
else:
    for doc in documents:
        # Generate a random timestamp in the specified range
        random_seconds = random.randint(0, int((end_time - start_time).total_seconds()))
        new_timestamp = start_time + timedelta(seconds=random_seconds)

        # ✅ Update the document with the new timestamp
        collection.update_one(
            {"_id": doc["_id"]},  # Find by document ID
            {"$set": {"timestamp": new_timestamp}}
        )

    print(f"✅ Successfully updated {len(documents)} records with new timestamps.")

# ✅ Close the MongoDB connection
client.close()
