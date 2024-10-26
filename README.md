# Sensor Fault Detection System

A machine learning-powered system for detecting anomalies in sensor data with load balancing capabilities. The system processes temperature, humidity, and loudness measurements to identify potential sensor faults in real-time.

## Features

- Real-time sensor data anomaly detection
- Load balancing across multiple server instances
- Simulation capabilities for testing
- REST API endpoints for data processing
- Machine learning model trained with Isolation Forest algorithm
- Data persistence using SQLite
- Configurable deployment settings

## System Architecture

The system consists of several key components:
- **Machine Learning Model**: Isolation Forest for anomaly detection
- **API Servers**: Multiple Flask instances handling sensor data
- **Load Balancer**: Round-robin distribution of requests
- **Data Generator**: Simulation of sensor readings
- **Database**: SQLite storage for sensor readings and predictions

## Prerequisites

- Python 3.x
- Flask and Flask-CORS
- scikit-learn
- pandas
- numpy
- requests
- joblib

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sensor-fault-detection
```

2. Install dependencies:
```bash
pip install requirements.txt
```
## Files Description

- `model.py`: Trains and saves the machine learning model
- `api.py`: Flask server for processing sensor data
- `processes.py`: Manages multiple server instances
- `load_balance.py`: Implements round-robin load balancing
- `generator.py`: Generates simulated sensor data

## Configuration

1. The `config.json` file can be used to select which model is used in the joblib format:
```json
{
  "model": "model.joblib",
  "scaler": "scaler.joblib",
  "score scaler": "score_scaler.joblib"
}
```

## Usage

### Training the Model

Run the model training script to generate the necessary model files:

```bash
python model.py
```

This will create:
- `model.joblib`: Trained Isolation Forest model
- `scaler.joblib`: StandardScaler for input normalization
- `score_scaler.joblib`: MinMaxScaler for anomaly scores
- `results.txt`: Model performance metrics

## Performance Metrics

The model's performance metrics include:
- Accuracy:0.95
- Precision:0.95
- Recall: ~1

These metrics are saved in `results.txt` after training.

### Starting the System

Launch the system using the processes script:

```bash
python processes.py
```

This will start:
- Two API servers on ports 5001 and 5002
- Load balancer on port 5000
- The results can be visualized locally on http://127.0.0.1:5000/

## Cloud
To use in cloud open the sites https://sensor-fault-detection-1.onrender.com and https://sensor-fault-detection-dg6k.onrender.com/ and open https://sensor-fault-detection-2.onrender.com the load balancer. Reload to redirect the load balancer to a different instance


