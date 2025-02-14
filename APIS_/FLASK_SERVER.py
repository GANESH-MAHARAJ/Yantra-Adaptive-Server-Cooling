import serial
import requests
import json
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# ============================
# 📌 Root Route: API Documentation
# ============================
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the Smart Cooling System API",
        "routes": {
            "/process_data": "POST - Receives sensor data from Arduino.",
            "/process_data": "GET - Allows AI agent to fetch latest sensor data.",
            "/receive_ai_response": "POST - Receives AI-generated response from Langflow."
        },
        "instructions": "Send POST requests to '/process_data' to store sensor data. AI agent can GET data from '/process_data' and POST its response to '/receive_ai_response'."
    })

# ============================
# 📌 Route 1: Receives AI response from Langflow
# ============================
@app.route('/receive_ai_response', methods=['POST'])
def receive_ai_response():
    try:
        data = request.json
        ai_text_response = data.get("ai_response", "")
        if not ai_text_response:
            return jsonify({"error": "No AI response received"}), 400
        print("Received AI Response:", ai_text_response)
        return jsonify({"status": "success", "message": "AI response received successfully", "ai_response": ai_text_response})
    except Exception as e:
        return jsonify({"error": f"Internal server error: {e}"}), 500

# ============================
# 📌 Route 2: Receives & Allows AI to Fetch Sensor Data
# ============================
latest_sensor_data = None  # Store the latest sensor data in memory

@app.route('/process_data', methods=['POST', 'GET'])
def process_data():
    global latest_sensor_data

    if request.method == 'POST':  # Receiving data from Arduino
        data = request.json
        print("Received data:", data)
        latest_sensor_data = data  # Store the latest sensor data
        return jsonify({"status": "success", "message": "Data processed successfully"})
    
    elif request.method == 'GET':  # Allow AI to fetch the latest data
        if latest_sensor_data is None:
            return jsonify({"error": "No sensor data available"}), 404
        return jsonify(latest_sensor_data)

# ============================
# 📌 Serial Communication with Arduino (Handles Missing Arduino)
# ============================
arduino_port = "COM14"  # Change to your correct port
baud_rate = 9600
api_url = "http://127.0.0.1:5000/process_data"

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to {arduino_port}")
    arduino_available = True
except serial.SerialException:
    print(f"Warning: Arduino not connected on {arduino_port}. Running Flask only.")
    arduino_available = False

def read_from_arduino():
    """Reads data from Arduino and sends it to Flask API."""
    if not arduino_available:
        print("Skipping Arduino reading (Not connected).")
        return
    
    while True:
        if ser.in_waiting:
            raw_data = ser.readline().decode("utf-8").strip()
            print("Received raw data:", raw_data)
            try:
                data_list = [value for value in raw_data.split() if value]
                if len(data_list) != 4:
                    print("Error: Incorrect data format.")
                    continue  # Skip invalid data
                sensor_data = [
                    {"temperature": float(data_list[0]), "humidity": float(data_list[2])},
                    {"temperature": float(data_list[1]), "humidity": float(data_list[3])}
                ]
                response = requests.post(api_url, json={"sensor_data": sensor_data})
                if response.status_code == 200:
                    print("Data successfully sent to Flask API")
                else:
                    print("Failed to send data. Status code:", response.status_code)
            except Exception as e:
                print(f"Error while parsing data: {e}")

# ============================
# 📌 Run Flask and Serial Reader in Parallel
# ============================
def run_flask():
    app.run(host='0.0.0.0', port=5000, use_reloader=False)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    if arduino_available: 
        read_from_arduino()  # Only start if Arduino is connected
