from flask import Flask, request, jsonify
import db

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Flask API!"

@app.route('/health_activities', methods=['POST'])
def add_health_activities():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    db.insert_data(data)
    return jsonify({"status": "success"}), 200

@app.route('/health_activities', methods=['GET'])
def get_health_activities():
    filters = request.args.to_dict()
    activities = db.fetch_all_data(filters)
    return jsonify(activities), 200

@app.route('/health_activities/<int:id>', methods=['PUT'])
def update_health_activity(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    success = db.update_data(id, data)
    if success:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "Entity not found"}), 404

@app.route('/health_activities/<int:id>', methods=['DELETE'])
def delete_health_activity(id):
    success = db.delete_data(id)
    if success:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "Entity not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
