import serial
import requests
import json
import time
import re  # For JSON extraction

# ✅ Arduino Serial Connection
arduino_port = "COM13"  # Change as needed
baud_rate = 9600  # Should match Arduino's Serial.begin(9600)

# ✅ Flask & AI API URLs
FLASK_API_URL = "http://127.0.0.1:5000/process_data"  # Flask server
AI_RESPONSE_API_URL = "http://127.0.0.1:5002/receive_ai_response"  # AI response API

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"✅ Connected to Arduino on {arduino_port}")
except serial.SerialException as e:
    print(f"❌ Error connecting to Arduino: {e}")
    exit()

def read_from_arduino():
    """Reads data from Arduino and formats it as structured JSON."""
    raw_data = ser.readline().decode("utf-8").strip()  # Read & decode
    print("📡 Received raw data:", raw_data)  # Debugging

    try:
        # Clean & split the incoming data
        data_list = [value for value in raw_data.split() if value]

        if len(data_list) != 10:
            print("❌ Incorrect data format. Expected 10 values.")
            return None

        # ✅ Format the data into previous and current states
        sensor_data = {
            "sensor_data": [
                [  # Previous state
                    {"temperature1.1": float(data_list[0]), "humidity1.1": float(data_list[1])},  # DataCube1 (Previous)
                    {"temperature2.1": float(data_list[2]), "humidity2.1": float(data_list[3])}   # DataCube2 (Previous)
                ],
                [  # Current state
                    {"temperature1.2": float(data_list[4]), "humidity1.2": float(data_list[5])},  # DataCube1 (Current)
                    {"temperature2.2": float(data_list[6]), "humidity2.2": float(data_list[7])}   # DataCube2 (Current)
                ],
                [  # Current Measurements
                    {"current1": float(data_list[8])},
                    {"current2": float(data_list[9])}
                ]
            ]
        }

        return sensor_data

    except Exception as e:
        print(f"❌ Error parsing data: {e}")
        return None

def send_fan_speed_to_arduino():
    """Fetch AI response and send fan speeds to Arduino."""
    try:
        # ✅ Step 1: Fetch AI Response
        response = requests.get(AI_RESPONSE_API_URL)
        if response.status_code == 200:
            ai_text_response = response.json().get("ai_response", "")
            if not ai_text_response:
                print("❌ No AI response received. Retrying...")
                return  # Skip this iteration

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

while True:
    # ✅ Step 1: Read Data from Arduino
    if True:
        sensor_data = read_from_arduino()
        # sensor_data= "20 20 20 20 20 20 20 20 20 20"

        if sensor_data:
            # ✅ Step 2: Send Sensor Data to Flask API
            flask_response = requests.post(FLASK_API_URL, json=sensor_data)
            if flask_response.status_code == 200:
                print("✅ Data successfully sent to Flask API")
            else:
                print("❌ Failed to send data. Status code:", flask_response.status_code)

    # ✅ Step 3: Fetch AI Response & Send Fan Speed to Arduino
    send_fan_speed_to_arduino()

    # ✅ Wait before next cycle
    time.sleep(3)
flask_response = requests.post(FLASK_API_URL, json=sensor_data)
