import json
import requests

# URLs
FLASK_API_URL = "http://127.0.0.1:5000/process_data"  # Flask API to fetch message
LANGFLOW_API_URL = "http://127.0.0.1:7860/api/v1/run/26c30bf4-134c-4843-86ac-6b278872cb70"  # Langflow API

# Fetch message from Flask API
flask_response = requests.get(FLASK_API_URL)

if flask_response.status_code == 200:
    message = flask_response.json() # Extract message
    if not message:
        print("Error: No 'message' found in Flask API response.")
        exit()
else:
    print("Error fetching message from Flask API:", flask_response.text)
    exit()

# Request payload for Langflow
payload = {
    "input_value": message,
    "output_type": "chat",
    "input_type": "chat"
}

# Send request to Langflow API
langflow_response = requests.post(LANGFLOW_API_URL, json=payload)

# Process response
if langflow_response.status_code == 200:
    result = langflow_response.json()
    print("Langflow API Output:", result)

    # Save output to file
    with open("langflow_output.json", "w") as f:
        json.dump(result, f, indent=4)

    print("Output saved to langflow_output.json")
else:
    print("Error from Langflow API:", langflow_response.text)
