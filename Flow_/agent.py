import json
import requests
import os

# URLs
FLASK_API_URL = "http://127.0.0.1:5000/process_data"  # Flask API to fetch sensor data
LANGFLOW_API_URL = "http://127.0.0.1:7860/api/v1/run/26c30bf4-134c-4843-86ac-6b278872cb70"  # Langflow API
AI_RESPONSE_API_URL = "http://127.0.0.1:5002/receive_ai_response"  # API to send AI response

# JSON log file name
JSON_LOG_FILE = "agent_output.json"

def save_json(data, filename=JSON_LOG_FILE):
    """Saves the latest AI response to a JSON file."""
    with open(filename, "w") as file:  # Overwrite with latest response
        json.dump(data, file, indent=4)
    print(f"📁 AI Response saved to {filename}")

while(True):
    # Step 1: Fetch message from Flask API
    flask_response = requests.get(FLASK_API_URL)

    if flask_response.status_code == 200:
        message = str(flask_response.json())  # Convert JSON to string
        if not message:
            print("❌ Error: No 'message' found in Flask API response.")
            exit()
    else:
        print("❌ Error fetching message from Flask API:", flask_response.text)
        exit()

    # Step 2: Send request to Langflow API
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat"
    }
    langflow_response = requests.post(LANGFLOW_API_URL, json=payload)

    if langflow_response.status_code == 200:
        result = langflow_response.json()

        # Step 3: Extract AI response message
        try:
            ai_response_text = result['outputs'][0]['outputs'][0]['results']['message']['text']
            print("✅ Langflow API Output:", ai_response_text)

            # Step 4: Save AI response to JSON file
            ai_response_data = {
                "flask_input": message,
                "ai_response": ai_response_text
            }
            save_json(ai_response_data)

            # Step 5: Send AI response to AI_RESPONSE_API_URL
            response_payload = {"ai_response": ai_response_text}
            response = requests.post(AI_RESPONSE_API_URL, json=response_payload)

            if response.status_code == 200:
                print("✅ Successfully sent AI response to the server.")
            else:
                print("❌ Error sending AI response:", response.text)

        except (KeyError, IndexError) as e:
            print(f"❌ Error extracting AI response: {e}")

    else:
        print("❌ Error from Langflow API:")

    print("\n🎉 Process completed! AI response saved and sent successfully.")

