import flask 

app = flask.Flask(__name__)

buzzer_on = False

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/check_buzzer_status", methods=["GET"])
def check_buzzer():
    """
    Checks the status of the buzzer by sending a GET request to the specified URL.
    
    Returns:
        dict: Parsed JSON response if successful, None otherwise.
    """

    global buzzer_on
    
    return flask.jsonify({"status": "OK", "buzzer_on": buzzer_on})

@app.route("/toggle_buzzer", methods=["GET"])
def toggle_buzzer():
    """
    Toggles the buzzer on or off by sending a POST request to the specified URL.
    
    Returns:
        dict: Parsed JSON response if successful, None otherwise.
    """

    global buzzer_on

    buzzer_on = not buzzer_on
    return flask.jsonify({"status": "OK", "buzzer_on": buzzer_on})

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)