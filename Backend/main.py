import flask 

app = flask.Flask(__name__)

alarm_on = False
bpm_list = []

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/check_alarm", methods=["GET"])
def check_alarm():
    """
    Checks the status of the buzzer by sending a GET request to the specified URL.
    
    Returns:
        dict: Parsed JSON response if successful, None otherwise.
    """

    global alarm_on
    
    return flask.jsonify({"status": "OK", "alarm_on": alarm_on})

@app.route("/toggle_alarm", methods=["GET"])
def toggle_alarm():
    """
    Toggles the buzzer on or off by sending a POST request to the specified URL.
    
    Returns:
        dict: Parsed JSON response if successful, None otherwise.
    """

    global alarm_on

    alarm_on = not alarm_on
    return flask.jsonify({"status": "OK", "alarm_on": alarm_on})

@app.route("/add_bpm", methods=["POST"])
def add_bpm():
    """
    Adds the BPM value to the database.
    
    Returns:
        dict: Parsed JSON response if successful, None otherwise.
    """

    bpm = flask.request.json.get("bpm")
    bpm_list.append(bpm)
    

    return flask.jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)