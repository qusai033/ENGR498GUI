from flask import Flask, jsonify, send_from_directory, request, abort
import pandas as pd
import os

app = Flask(__name__)

# Path to the directory containing device folders
DATA_DIRECTORY = './data'

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

# Endpoint to list all devices (subdirectories in the DATA_DIRECTORY)
@app.route('/list_devices', methods=['GET'])
def list_devices():
    try:
        # List all directories (devices) within the DATA_DIRECTORY
        devices = [d for d in os.listdir(DATA_DIRECTORY) if os.path.isdir(os.path.join(DATA_DIRECTORY, d))]
        return jsonify(devices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get voltage data for a specific device
@app.route('/data/<device>/voltageData.txt', methods=['GET'])
def get_voltage_data(device):
    file_path = os.path.join(DATA_DIRECTORY, device, 'voltageData.txt')
    
    if not os.path.exists(file_path):
        return abort(404, description="Voltage data file not found.")
    
    # Read the voltage data file as plain text
    with open(file_path, 'r') as f:
        data = f.read()
    
    return data

# Endpoint to get RUL (Remaining Useful Life) data for a specific device
@app.route('/data/<device>/rulData.csv', methods=['GET'])
def get_rul_data(device):
    file_path = os.path.join(DATA_DIRECTORY, device, 'rulData.csv')
    
    if not os.path.exists(file_path):
        return abort(404, description="RUL data file not found.")
    
    # Load the CSV data into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Check if the necessary columns exist in the CSV
    if 'DT' not in df.columns or 'RUL' not in df.columns:
        return abort(400, description="CSV file must contain 'DT' and 'RUL' columns.")
    
    # Convert the DataFrame to a dictionary suitable for JSON
    data = {
        "time": df['DT'].tolist(),
        "rul": df['RUL'].tolist()
    }
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
