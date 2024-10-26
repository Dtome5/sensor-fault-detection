import subprocess
import signal
import sys

# List to keep track of all the processes
processes = []


# Function to kill all processes
def cleanup_processes():
    print("Terminating all processes...")
    for process in processes:
        process.terminate()  # Gracefully terminate the process
        process.wait()  # Wait for the process to terminate
    print("All processes terminated.")


# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    cleanup_processes()
    sys.exit(0)


# Register the signal handler for SIGINT (Ctrl+C) and SIGTERM
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    # Run the first instance of api.py on port 5001
    p1 = subprocess.Popen(["uv", "run", "api.py", "5001"])
    processes.append(p1)

    # Run the second instance of api.py on port 5002
    p2 = subprocess.Popen(["uv", "run", "api.py", "5002"])
    processes.append(p2)

    # Run load_balance.py on port 5000
    p3 = subprocess.Popen(["uv", "run", "load_balance.py", "5000"])
    processes.append(p3)

    # Wait indefinitely for processes to run
    while True:
        pass

except Exception as e:
    print(f"An error occurred: {e}")
    cleanup_processes()
    sys.exit(1)
