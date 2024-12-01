import flask
from flask import jsonify
from celery import Celery
from celery.py import make_celery

app = flask.Flask(__name__)

# Initialize Celery
celery = make_celery(app)

alarm_on = False
bpm_list = []
drowsy_ratio = 0.0  # Initial value

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
    Returns the current drowsy ratio by querying the Celery task result.
    """
    result = fetch_drowsy_ratio_task.apply_async()
    drowsy_ratio = result.get()  # Wait for task completion
    return jsonify({"status": "OK", "drowsy_ratio": drowsy_ratio})


@celery.task
def fetch_drowsy_ratio_task():
    """
    Task to retrieve the current drowsy ratio from the shared data.
    """
    # In practice, you can fetch this from a shared data store or calculate dynamically
    return shared_data["drowsy_ratio"]


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
