from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store user-wise voice inputs
user_text_store = {}

@app.route("/receive", methods=["POST"])
def receive():
    data = request.get_json()
    user_id = data.get("user_id")
    text = data.get("text")

    if not user_id or not text:
        return jsonify({"status": "error", "message": "Missing user_id or text"}), 400

    user_text_store[user_id] = text
    print(f"✅ Received from {user_id}: '{text}'")
    return jsonify({"status": "received", "text": text})

@app.route("/latest", methods=["GET"])
def latest():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"status": "error", "message": "Missing user_id"}), 400

    return jsonify({"text": user_text_store.get(user_id, "")})

@app.route("/clear", methods=["POST"])
def clear():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"status": "error", "message": "Missing user_id"}), 400

    user_text_store[user_id] = ""
    print(f"🗑️ Cleared input for {user_id}")
    return jsonify({"status": "cleared"})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "status": "running",
        "users": list(user_text_store.keys())
    })

if __name__ == "__main__":
    print("🎙️ Voice API Server starting...")
    print("📡 Server running at http://0.0.0.0:5001")
    print("🔗 Endpoints:")
    print("   POST /receive - Receive voice input")
    print("   GET  /latest  - Get latest voice input")
    print("   POST /clear   - Clear stored input")
    print("   GET  /status  - Check server status")
    app.run(host="0.0.0.0", port=5001, debug=True)
