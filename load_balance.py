from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# List of backend servers
backend_servers = [
    "https://sensor-fault-detection.onrender.com",  # Backend server 1
    "https://sensor-fault-detection-1.onrender.com",  # Backend server 3
]

# Index to keep track of the round-robin rotation
server_index = 0


def get_next_server():
    """Simple round-robin logic to get the next server."""
    global server_index
    server = backend_servers[server_index]
    server_index = (server_index + 1) % len(backend_servers)  # Rotate index
    return server


@app.route("/balance", methods=["POST", "GET"])
def load_balance():
    """Main load balancer route, forwards requests to one of the backend servers."""
    target_server = get_next_server()

    # Forward the request to the selected backend server
    if request.method == "POST":
        response = requests.post(target_server + request.path, json=request.json)
    else:
        response = requests.get(target_server + request.path)

    # Return the response from the backend server
    return jsonify(response.json()), response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
