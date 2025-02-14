import json
import requests
import pymongo
import re  # For extracting JSON from response text
from datetime import datetime  # For timestamp
import time  # For delay between requests

# ✅ MongoDB Setup
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "SmartCoolingSystem"
COLLECTION_NAME = "Processed_AI_Responses"

# ✅ API URLs
AI_RESPONSE_API_URL = "http://127.0.0.1:5002/receive_ai_response"

# ✅ Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

print("✅ Connected to MongoDB!")

# ✅ Keep track of last stored response to avoid duplicates
last_stored_response = None  

while True:
    try:
        # ✅ Step 1: Fetch AI Response from API
        response = requests.get(AI_RESPONSE_API_URL)

        if response.status_code == 200:
            ai_text_response = response.json().get("ai_response", "")

            if not ai_text_response:
                print("❌ No AI response received. Retrying...")
                time.sleep(2)  # Wait & retry
                continue  

            # ✅ Avoid storing duplicate responses
            if ai_text_response == last_stored_response:
                print("⚠️ Skipping duplicate response.")
                time.sleep(2)  # Wait & retry
                continue  
            
            print("✅ Raw AI Response:", ai_text_response)

            # ✅ Step 2: Extract JSON Data from AI Response
            json_pattern = r"\[\s*\[.*?\]\s*\]"  # Regex pattern to extract JSON list
            match = re.search(json_pattern, ai_text_response, re.DOTALL)

            if match:
                ai_json_string = match.group(0)  # Extract the matched JSON
                try:
                    ai_data = json.loads(ai_json_string)  # Convert string to JSON
                    print("✅ Extracted AI JSON:", ai_data)

                    # ✅ Step 3: Process Data & Create Structured Format
                    processed_data = []
                    for i, data_cube in enumerate(ai_data):
                        structured_record = {
                            "data_cube": i + 1,
                            "fan_speed": data_cube[0],
                            "humidity": data_cube[1],
                            "heat": data_cube[2],
                            "temperature": data_cube[3][0],  # Extract temperature
                            "current": data_cube[3][1],  # Extract current
                            "ai_suggestion": data_cube[4],
                            "timestamp": datetime.utcnow().isoformat()  # Store current time in UTC
                        }
                        processed_data.append(structured_record)

                    print("✅ Processed Data:", json.dumps(processed_data, indent=2))

                    # ✅ Step 4: Store in MongoDB
                    collection.insert_many(processed_data)
                    print("✅ Successfully stored structured data in MongoDB!")

                    # ✅ Update last stored response
                    last_stored_response = ai_text_response

                except json.JSONDecodeError:
                    print("❌ Error: Failed to decode JSON.")
            else:
                print("❌ Error: Could not extract JSON from AI response.")

        else:
            pass

    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")

    # ✅ Wait before next API call (avoid overloading)
    # time.sleep(3)  # Fetch new data every 3 seconds
