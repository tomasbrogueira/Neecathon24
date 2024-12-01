import flask
from flask import jsonify
import threading

app = flask.Flask(__name__)

# Shared variables
shared_data = {"drowsy_ratio": 0.0}  # Initial drowsy ratio
lock = threading.Lock()
alarm_on = False
bpm_list = []

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/check_alarm", methods=["GET"])
def check_alarm():
    global alarm_on
    return jsonify({"status": "OK", "alarm_on": alarm_on})

@app.route("/toggle_alarm", methods=["GET"])
def toggle_alarm():
    global alarm_on
    alarm_on = not alarm_on
    return jsonify({"status": "OK", "alarm_on": alarm_on})

@app.route("/add_bpm", methods=["POST"])
def add_bpm():
    bpm = flask.request.json.get("bpm")
    bpm_list.append(bpm)
    return jsonify({"status": "OK"})

@app.route("/get_drowsy_ratio", methods=["GET"])
def get_drowsy_ratio():
    """
    Returns the current drowsy ratio value.
    """
    with lock:
        current_ratio = shared_data["drowsy_ratio"]
    return jsonify({"status": "OK", "drowsy_ratio": current_ratio})

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
