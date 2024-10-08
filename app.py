import os
from flask import Flask, render_template, send_from_directory, jsonify, abort

app = Flask(__name__)

# Path to the directory containing device folders
BASE_DEVICE_DIRECTORY = './data'  # Relative to your project directory on Replit


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data/<device>/<filename>', methods=['GET'])
def get_data_file(device, filename):
    device_folder_path = os.path.join(BASE_DEVICE_DIRECTORY, device)

    # Ensure the device folder exists
    if not os.path.exists(device_folder_path):
        return abort(404, description="Device not found")

    # Ensure the file exists in the device folder
    if not os.path.exists(os.path.join(device_folder_path, filename)):
        return abort(404, description="File not found")

    # Serve the file from the device folder
    return send_from_directory(device_folder_path, filename)


@app.route('/list_devices', methods=['GET'])
def list_devices():
    # List all directories (devices) within the BASE_DEVICE_DIRECTORY
    devices = [f.name for f in os.scandir(BASE_DEVICE_DIRECTORY) if f.is_dir()]
    return jsonify(devices)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
