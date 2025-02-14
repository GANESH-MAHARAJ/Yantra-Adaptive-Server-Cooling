from pymongo import MongoClient
import random
from datetime import datetime, timedelta

# 🔹 MongoDB Connection
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "SmartCoolingSystem"  # Change this to your actual database name
COLLECTION_NAME = "Processed_AI_Responses"  # Change this to your actual collection name

# ✅ Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# 🔹 Define Time Range
start_time = datetime(2025, 2, 8, 23, 0, 0)  # Feb 8, 2025, 23:00
end_time = datetime(2025, 2, 9, 14, 0, 0)    # Feb 9, 2025, 14:00

# 🔹 Generate Fake Data
num_entries = 100  # Adjust number of data points

fake_data = []
for _ in range(num_entries):
    # ✅ Generate a completely random timestamp within the range
    random_seconds = random.randint(0, int((end_time - start_time).total_seconds()))
    timestamp = start_time + timedelta(seconds=random_seconds)

    data_cube = random.choice([1, 2])  # Randomly assign DataCube 1 or 2
    temperature = round(random.uniform(20, 40), 2)  # Temp between 20°C and 40°C
    humidity = round(random.uniform(50, 80), 2)  # Humidity between 50% and 80%
    fan_speed = random.randint(50, 220)  # Fan speed between 50-220
    heat = round((temperature - 20) * 0.5, 2)  # Fake heat calculation
    current = random.randint(50, 100)  # Current consumption between 50-100
    ai_suggestion = f"AI Suggestion: {'Optimal' if fan_speed < 180 else 'Reduce speed'}"

    fake_data.append({
        "timestamp": timestamp.isoformat(),  # ✅ Store as ISO format for MongoDB
        "data_cube": data_cube,
        "temperature": temperature,
        "humidity": humidity,
        "fan_speed": fan_speed,
        "heat": heat,
        "current": current,
        "ai_suggestion": ai_suggestion
    })

# ✅ Insert Data into MongoDB
collection.insert_many(fake_data)
print(f"✅ Inserted {num_entries} fake data entries with **random timestamps** into MongoDB.")

# Close MongoDB Connection
client.close()
