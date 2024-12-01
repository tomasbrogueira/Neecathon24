import flask
from flask import jsonify

app = flask.Flask(__name__)

alarm_on = False
bpm_list = []
DROWSY_TREASHOLD = 0.8

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/check_alarm", methods=["GET"])
def check_alarm():
    global alarm_on

    drowsy_ratio = 0
    with open("drowsy_ratio.txt", "r") as f:
        drowsy_ratio = float(f.read())

    if drowsy_ratio > DROWSY_TREASHOLD:
        alarm_on = True
    else:
        alarm_on = False

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
    Returns the current drowsy ratio by querying the Celery task result.
    """
    drowsy_ratio = 0
    with open("drowsy_ratio.txt", "r") as f:
        drowsy_ratio = float(f.read())

    return jsonify({"status": "OK", "drowsy_ratio": drowsy_ratio})

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
