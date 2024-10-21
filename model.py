# from numpy.random.mtrand import logistic
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
from joblib import dump
import mlflow.sklearn
import pickle

# import mlflow


class ScaledIsolationForest:
    def __init__(self, base_model, score_range=(0, 100)):
        self.base_model = base_model
        self.score_scaler = MinMaxScaler(feature_range=score_range)
        self.decision_scaler = MinMaxScaler(feature_range=score_range)

    def fit(self, X):
        # Get raw scores and decisions
        raw_scores = -self.base_model.score_samples(X)
        raw_decisions = -self.base_model.decision_function(X)

        # Fit scalers
        self.score_scaler.fit(raw_scores.reshape(-1, 1))
        self.decision_scaler.fit(raw_decisions.reshape(-1, 1))

    def get_scaled_score(self, X):
        raw_scores = -self.base_model.score_samples(X)
        return self.score_scaler.transform(raw_scores.reshape(-1, 1)).ravel()

    def get_scaled_decision(self, X):
        raw_decisions = -self.base_model.decision_function(X)
        return self.decision_scaler.transform(raw_decisions.reshape(-1, 1)).ravel()


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

# the models confusion matrix
cnf_matrix = confusion_matrix(
    np.array(list(map(lambda x: 1 if x == False else -1, y_test))), y_pred
)
# print(cnf_matrix)
# print(model.decision_function(scaler.transform([[23, 23, 230]])))
# print(y_pred)
# print(x_train)

# save model to file
dump(model, "model.joblib")
dump(scaler, "scaler.joblib")


scaled_model = ScaledIsolationForest(model)
scaled_model.fit(x_train)
dump(scaled_model, "score.joblib")

max = scaler.transform([[-1000, 10000, 1000]])
min = scaler.transform([[35, 50, 80]])
print(scaled_model.get_scaled_score(max))
print(model.score_samples(max))
print(model.decision_function(min))
print(model.score_samples(min))
