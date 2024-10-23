import json
import os
import sqlite3
from generator import simulate
from joblib import load
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
with open("config.json") as config_file:
    config = json.load(config_file)
CORS(app)

con = sqlite3.connect("database.db", check_same_thread=False)
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS Data(Id,Temperature,Humidity,Loudness,Prediction,AnomalyScore )"
)
id = 0
print(os.getenv("PROD"))
local_url = "http://localhost:5000"
url = (
    # config["api_url"]
    os.getenv("URL")
    if bool(os.getenv("URL"))
    else local_url
)

loaded_model = load(config["model"])
scaler = load(config["scaler"])
score_scaler = load(config["score scaler"])


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
    global id
    id += 1
    simulated_data = simulate() + [id]
    return jsonify({"simulated_data": simulated_data})


@app.route("/sensors", methods=["POST"])
def index_post():
    # global id
    data = request.json
    sensor_data = data["sensor_data"]
    temperature = sensor_data[0]
    humidity = sensor_data[1]
    loudness = sensor_data[2]
    predictions, anomaly_score = prediction(sensor_data[:3])
    result_str = "Anomaly" if predictions[0] == -1 else "Normal"
    cur.execute(
        "INSERT INTO Data VALUES(?,?,?,?,?,?)",
        (id, temperature, humidity, loudness, result_str, int(anomaly_score[0][0])),
    )
    response = {
        "sensor_data": {
            "id": id,
            "temperature": sensor_data[0],
            "humidity": sensor_data[1],
            "loudness": sensor_data[2],
            "prediction": result_str,
            "anomaly_score": anomaly_score[0][0],
        }
    }

    json.dumps(response, indent=2)
    con.commit()

    return jsonify(response)


if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT")) if bool(os.getenv("PORT")) else 5000)
