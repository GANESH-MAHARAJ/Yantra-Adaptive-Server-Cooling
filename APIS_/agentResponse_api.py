import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
latest_ai_response = None  # Store latest AI response in memory

@app.route('/receive_ai_response', methods=['POST', 'GET'])
def receive_ai_response():
    """Handles AI-generated responses (POST) and allows retrieval (GET)."""
    
    global latest_ai_response

    if request.method == 'POST':  # Receiving AI response from Langflow
        try:
            data = request.json
            ai_text_response = data.get("ai_response", "")

            if not ai_text_response:
                return jsonify({"error": "No AI response received"}), 400

            print("\n✅ Received AI Response from Langflow:")
            print(ai_text_response)

            # ✅ Store latest AI response (but DO NOT forward it to itself!)
            latest_ai_response = ai_text_response

            return jsonify({
                "status": "success",
                "message": "AI response received successfully",
                "ai_response": ai_text_response
            })

        except Exception as e:
            print(f"Error while processing AI response: {e}")
            return jsonify({"error": f"Internal server error: {e}"}), 500

    elif request.method == 'GET':  # Fetch latest AI response
        if latest_ai_response is None:
            return jsonify({"error": "No AI response available"}), 404

        print("\n📌 Latest AI Response Sent to Browser:")
        print(latest_ai_response)

        return jsonify({
            "status": "success",
            "ai_response": latest_ai_response
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)  # Running on port 5002

