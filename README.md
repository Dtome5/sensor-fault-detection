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


## Configuration

1. The `config.json` file has the following structure:
```json
{
  "model": "model.joblib",
  "scaler": "scaler.joblib",
  "score scaler": "score_scaler.joblib"
}
```

2. Environment Variables (optional):
- `PROD`: Production environment flag
- `PORT`: Server port number
- `URL`: Backend server URL

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

### Starting the System

Launch the system using the processes script:

```bash
python processes.py
```

This will start:
- Two API servers on ports 5001 and 5002
- Load balancer on port 5000

### API Endpoints

1. Root endpoint:
```
GET /
```
Returns the home page

2. Simulation endpoint:
```
GET /simulate
```
Returns simulated sensor data

3. Sensor data processing:
```
POST /sensors
{
    "sensor_data": [temperature, humidity, loudness]
}
```
Returns prediction results including:
- Prediction (Normal/Anomaly)
- Anomaly score
- Sensor readings

## Data Format

Sensor data should be provided as an array with three values:
1. Temperature (°C): Expected range 20-50
2. Humidity (%): Expected range 30-70
3. Loudness (dB): Expected range 60-100

Values outside these ranges are more likely to be classified as anomalies.

## Development

The system can be run in development mode using local URLs by not setting the `URL` environment variable. For production, set the appropriate environment variables and update the backend server URLs in `load_balance.py`.
## Cloud
To use in cloud open the sites https://sensor-fault-detection-1.onrender.com and https://sensor-fault-detection-dg6k.onrender.com/ and open https://sensor-fault-detection-2.onrender.com the load balancer. Reload to redirect the load balancer to a different instance

## Files Description

- `model.py`: Trains and saves the machine learning model
- `api.py`: Flask server for processing sensor data
- `processes.py`: Manages multiple server instances
- `load_balance.py`: Implements round-robin load balancing
- `generator.py`: Generates simulated sensor data

## Performance Metrics

The model's performance metrics include:
- Accuracy:0.95
- Precision:0.95
- Recall: ~1

These metrics are saved in `results.txt` after training.

