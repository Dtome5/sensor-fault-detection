import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
)
from sklearn import model_selection
from joblib import dump
import mlflow.sklearn

# loads data from csv
data = pd.read_csv("sim_data.csv", index_col=False)
data["temp"] = data["temp"].astype(float)
data["hum"] = data["hum"].astype(float)
data["dec"] = data["dec"].astype(float)

# transform data to numpy array
data = data.to_numpy()

# scales data
scaler = StandardScaler()
data[:, :3] = scaler.fit_transform(data[:, :3])

# separates data into input and output values
x = data[:, :3]
y = data[:, 3]

# splits training and testing data
x_train, x_test, y_train, y_test = train_test_split(x, y)

# fit the isolationforest model with data
model = IsolationForest(random_state=0)
model.fit(x_train, y_train)

# testing model
y_pred = model.predict(x_test)

# confusion matrix
cnf_matrix = confusion_matrix(
    np.array(list(map(lambda x: 1 if x == False else -1, y_test))), y_pred
)
y = np.array(list(map(lambda x: 1 if x == False else -1, y)))

y_test = np.array(list(map(lambda x: 1 if x == False else -1, y_test)))

kfold = model_selection.KFold(shuffle=True, random_state=0)

accuracy = model_selection.cross_val_score(model, x, y=y, cv=kfold, scoring="accuracy")

recall = recall_score(y_test, y_pred)

precision = precision_score(y_test, y_pred)

print(f"accuracy: {accuracy.mean()}\nprecision: {precision}\n recall: {recall}")

predictions = model.decision_function(x)
min_max = MinMaxScaler(feature_range=(0, 100))
min_max.fit(predictions.reshape(-1, 1))

results = {
    "precision": precision_score(y_test, y_pred),
    "recall": recall_score(y_test, y_pred),
    "accuaracy": accuracy.mean(),
    "confusion_matrix": cnf_matrix,
}
# save results to file
with open("results.txt", "w") as result:
    result.write(json.dumps(results, indent=2))
# save model and scalers
dump(model, "model.joblib")
dump(scaler, "scaler.joblib")
dump(min_max, "score_scaler.joblib")
