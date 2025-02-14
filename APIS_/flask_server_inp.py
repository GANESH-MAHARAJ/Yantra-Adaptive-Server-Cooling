from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
latest_sensor_data = None  # Store the latest sensor data

@app.route('/process_data', methods=['POST', 'GET'])
def process_data():
    global latest_sensor_data

    if request.method == 'POST':  # Receiving sensor data
        data = request.json
        latest_sensor_data = data  # Store latest data
        # print(latest_sensor_data)
        return jsonify({"status": "success", "message": "Data processed successfully"})

    elif request.method == 'GET':  # Fetch latest sensor data
        if latest_sensor_data is None:
            return jsonify({"error": "No sensor data available"}), 404
        # print(latest_sensor_data,"wd")
        return jsonify(latest_sensor_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Flask app will run on http://127.0.0.1:5000/process_data
