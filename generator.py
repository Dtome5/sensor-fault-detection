#!/usr/bin/env python
# encoding: utf-8
import random
import requests
import time
import csv
import pandas as pd
import numpy as np
import json
from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
import threading
from joblib import load

app = Flask(__name__)


# function for generating predictions
def pred_model(y):
    loaded_model = load("model.joblib")
    scaler = load("scaler.joblib")
    score = load("score_scaler.joblib")
    scaled_data = scaler.transform([y])
    percentages = 100 - score.transform(loaded_model.decision_function(scaled_data).reshape(1,-1))
    print(loaded_model.decision_function(scaled_data))
    return loaded_model.predict(scaled_data), percentages


@app.route("/sensors", methods=["POST"])
def index_post():
    # receive sensor data
    data = request.json
    sensor_data = data["sensor_data"]
    prediction, percent = pred_model(sensor_data)
    result_str = "Anomaly" if prediction[0] == -1 else "Normal"
    result = json.dumps(
        {
            "input_data": data["sensor_data"],
            "prediction": result_str,
            "anomaly_score": str(prediction),
            "percent": str(percent),
        },indent= 2
    )
    print(result)
    return result


# @app.route("/")
# def index():
#     return render_template("home.html")


def fault(temp, hum, dec):
    # checks if the parameters are within reasonable limits
    if 20 <= temp <= 50 and 30 <= hum <= 70 and 60 <= dec <= 100:
        return False
    else:
        return True


# generates random values for humidity
def temp():
    rand = random.random()
    if rand < 0.9:
        return round(random.uniform(20, 50), 2)
    else:
        return round(random.uniform(-50, 200), 2)


# generates random values for humidity
def humidity():
    rand = random.random()
    if rand < 0.9:
        return random.randint(30, 70)
    else:
        return random.randint(0, 100)


# generate random values for loudness
def decibels():
    rand = random.random()
    if rand < 0.9:
        return random.randint(60, 100)
    else:
        return random.randint(0, 150)


# function to generate random values for a single unit
def simulate(fault=False):
    units = [temp(), humidity(), decibels()]
    if fault:
        pd.concat([units, fault(units[0], units[1], units[2])], axis=1)
    return units


# posts data to url
def send_data(url, data):
    payload = {"sensor_data": data}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        print(f"Sent data: {data}")
        print(f"Received response: {response.json()}")
        print(f"Response text:{response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")


def main():
    api_url = "http://127.0.0.1:5000/sensors"
    sensor_data = simulate()
    no_requests = 100
    for i in range(no_requests):
        sensor_data = simulate()
        time.sleep(2)
        send_data(api_url, sensor_data)


threads = threading.Thread(target=main, daemon=True)
if __name__ == "__main__":
    threads.start()
    app.run()
"""
df = pd.DataFrame(simulate())
df._append(simulate())
# print(df, "\n", simulate())
df.to_csv("newcsv.csv", index=False)

# generate 5000 random values and save them into a dataframe
with open("sim_data.csv", "w", newline="") as sim_csv:
    cswriter = csv.writer(sim_csv)
    cswriter.writerow(["temp", "hum", "dec", "fault"])
    for i in range(1, 5000):
        cswriter.writerow(simulate())
"""
