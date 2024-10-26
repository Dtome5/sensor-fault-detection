from flask import Flask, request, jsonify
import sys, os
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# List of backend servers
backend_servers = (
    [
        "https://sensor-fault-detection-dg6k.onrender.com",  # Backend server 1
        "https://sensor-fault-detection-1.onrender.com",  # Backend server 3
    ]
    if bool(os.getenv("URL"))
    else ["http://localhost:5001", "http://localhost:5002"]
)

# Index to keep track of the round-robin rotation
server_index = 0


def get_next_server():
    """Simple round-robin logic to get the next server."""
    global server_index
    server = backend_servers[server_index]
    server_index = (server_index + 1) % len(backend_servers)
    print(f"{server_index}, {backend_servers}")  # Rotate index
    return server


@app.route("/", methods=["POST", "GET"])
def load_balance():
    """Main load balancer route, forwards requests to one of the backend servers."""
    target_server = get_next_server()

    accept_header = request.headers.get("Accept", "")

    # Log the target server and request information for debugging
    print(
        f"to {target_server} \n request path: {request.path} \n request json: {request.json if request.is_json else 'No JSON'}"
    )

    # Forward the request based on the media type
    if "application/json" in accept_header:
        # Handle JSON requests
        print("was json")
        if request.method == "POST":
            response = requests.post(target_server + request.path, json=request.json)
        else:
            response = requests.get(target_server + request.path)
        print(response)

        # Return the JSON response from the backend server
        return jsonify(response.json()), response.status_code

    elif "text/html" in accept_header:
        # Handle HTML requests
        print("was html")

        if request.method == "POST":
            response = requests.post(target_server + request.path, data=request.data)
        else:
            response = requests.get(target_server + request.path)
        print(response)

        # Return the HTML response from the backend server
        return response.text, response.status_code

    else:
        # Default case for unsupported media types
        return jsonify({"error": "Unsupported media type"}), 415


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", int(sys.argv[1]))))
