from flask import Flask, jsonify, render_template, request, abort
import os

app = Flask(__name__)

# Path to the base data directory
BASE_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), '../data'))  # Relative to the script
os.makedirs(BASE_DIRECTORY, exist_ok=True)  # Ensure base directory exists

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Check for an allowed file format
    if file and allowed_file(file.filename):
        # Extract the device name from the query parameter
        device = request.form.get('device')
        if not device:
            return jsonify({"error": "Device name not provided."}), 400

        # Define the save path (data/device/voltage_log)
        device_folder = os.path.join(BASE_DIRECTORY, device)
        voltage_log_folder = os.path.join(device_folder, 'voltage_log')
        os.makedirs(voltage_log_folder, exist_ok=True)  # Create directories if they don't exist

        # Save the file to the voltage_log folder
        save_path = os.path.join(voltage_log_folder, file.filename)
        try:
            file.save(save_path)
            return jsonify({"message": f"File '{file.filename}' uploaded successfully to '{voltage_log_folder}'."}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to save the file: {str(e)}"}), 500

    return jsonify({"error": "Invalid file format. Only .csv files are allowed."}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
