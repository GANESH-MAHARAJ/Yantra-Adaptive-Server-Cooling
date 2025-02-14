import time
import requests

# ✅ Use the correct Flow ID from Langflow
FLOW_ID = "26c30bf4-134c-4843-86ac-6b278872cb70"
LANGFLOW_API_URL = f"http://127.0.0.1:7860/api/v1/run/{FLOW_ID}"  # ✅ Correct endpoint

# Flask API where AI response will be sent
FLASK_API_URL = "http://127.0.0.1:5002/receive_ai_response"

def call_langflow():
    """Sends request to Langflow AI agent and forwards response to Flask API."""
    try:
        # 1️⃣ Call Langflow to get AI-generated response (Use POST)
        langflow_response = requests.post(LANGFLOW_API_URL, json={})  # ✅ Use POST

        if langflow_response.status_code == 200:
            ai_response = langflow_response.json()
            print("\n✅ AI Response from Langflow:", ai_response)

            # 2️⃣ Forward AI response to Flask API
            flask_response = requests.post(FLASK_API_URL, json={"ai_response": ai_response})

            if flask_response.status_code == 200:
                print("✅ AI Response Sent to Flask API")
            else:
                print("❌ Error Sending AI Response to Flask:", flask_response.text)

        else:
            print("❌ Error Calling Langflow:", langflow_response.text)

    except Exception as e:
        print("❌ Exception:", e)

# Run AI agent continuously every 10 seconds
while True:
    call_langflow()
    time.sleep(10)  # Wait 10 seconds before next execution
