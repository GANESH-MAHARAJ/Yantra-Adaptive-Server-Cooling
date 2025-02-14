import serial
import requests
import json
import time

# ✅ Arduino Serial Connection
arduino_port = "COM13"  # Change to the correct port
baud_rate = 9600  # Should match Arduino's Serial.begin(9600)
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
print(f"✅ Connected to Arduino on {arduino_port}")

# ✅ AI Response API
AI_RESPONSE_API_URL = "http://127.0.0.1:5002/receive_ai_response"

while True:
    try:
        # ✅ Step 1: Fetch AI Response
        response = requests.get(AI_RESPONSE_API_URL)
        if response.status_code == 200:
            ai_text_response = response.json().get("ai_response", "")
            if not ai_text_response:
                print("❌ No AI response received. Retrying...")
                time.sleep(2)
                continue  # Skip this iteration

            print("✅ Raw AI Response:", ai_text_response)

            # ✅ Step 2: Extract JSON Data from AI Response
            json_pattern = r"\[\s*\[.*?\]\s*\]"  # Regex pattern to extract JSON list
            match = re.search(json_pattern, ai_text_response, re.DOTALL)

            if match:
                ai_json_string = match.group(0)  # Extract the matched JSON
                try:
                    ai_data = json.loads(ai_json_string)  # Convert string to JSON
                    print("✅ Extracted AI JSON:", ai_data)

                    # ✅ Step 3: Extract Fan Speed & Format Data
                    fan_speed_commands = []
                    for i, data_cube in enumerate(ai_data):
                        fan_speed = data_cube[0]  # Extract fan speed
                        formatted_command = f"{i+1} {fan_speed}"  # "1 100", "2 50"
                        fan_speed_commands.append(formatted_command)

                    print("✅ Fan Speed Commands:", fan_speed_commands)

                    # ✅ Step 4: Send Commands to Arduino via Serial
                    for command in fan_speed_commands:
                        ser.write((command + "\n").encode())  # Send command
                        print(f"📡 Sent to Arduino: {command}")
                        time.sleep(1)  # Small delay to ensure smooth communication

                except json.JSONDecodeError:
                    print("❌ Error: Failed to decode JSON.")
            else:
                print("❌ Error: Could not extract JSON from AI response.")

        else:
            print("❌ Error fetching AI response:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")

    # ✅ Wait before next API call
    time.sleep(3)  # Fetch new data every 3 seconds
