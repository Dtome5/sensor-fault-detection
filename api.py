import json
import os
from generator import simulate
from joblib import load
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
with open("config.json") as config_file:
    config = json.load(config_file)
CORS(app)

url = (
    config["api_url"]
    if os.getenv("PROD", "no").lower() == "yes"
    else "http://localhost:5000"
)

loaded_model = load("model.joblib")
scaler = load("scaler.joblib")
score_scaler = load("score_scaler.joblib")


# generates predictions
def prediction(x):
    scaled_data = scaler.transform([x])
    score = 100 - score_scaler.transform(
        loaded_model.decision_function(scaled_data).reshape(1, -1)
    )
    return loaded_model.predict(scaled_data), score


@app.route("/")
def index():
    return render_template("home.html", url=url)


@app.route("/simulate")
def index_simulate():
    simulated_data = simulate()
    return jsonify({"simulated_data": simulated_data})


@app.route("/sensors", methods=["POST"])
def index_post():
    data = request.json
    sensor_data = data["sensor_data"]
    predictions, anomaly_score = prediction(sensor_data)
    result_str = "Anomaly" if predictions[0] == -1 else "Normal"
    print(sensor_data)
    response = {
        "sensor_data": {
            "id": id,
            "temperature": sensor_data[0],
            "humidity": sensor_data[1],
            "loudness": sensor_data[2],
            "prediction": result_str,
            "percent": anomaly_score[0][0],
        }
    }

    json.dumps(response, indent=2)

    return jsonify(response)


if __name__ == "__main__":
    app.run()
