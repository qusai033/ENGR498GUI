from flask import Flask, jsonify, render_template, request, abort
import pandas as pd
import os

app = Flask(__name__)

# Path to the directory containing device folders
DATA_DIRECTORY = '../data'  # Relative path to the data folder

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to list all devices (subdirectories in the DATA_DIRECTORY)
@app.route('/list_devices', methods=['GET'])
def list_devices():
    try:
        devices = [d for d in os.listdir(DATA_DIRECTORY) if os.path.isdir(os.path.join(DATA_DIRECTORY, d))]
        return jsonify(devices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get voltage data for a specific device
@app.route('/data/<device>/voltageData.csv', methods=['GET'])
def get_voltage_data(device):
    file_path = os.path.join(DATA_DIRECTORY, device, 'voltageData.csv')
    
    if not os.path.exists(file_path):
        return abort(404, description="Voltage data file not found.")
    
    df = pd.read_csv(file_path)
    if 'Time' not in df.columns or 'Voltage' not in df.columns:
        return abort(400, description="CSV file must contain 'Time' and 'Voltage' columns.")
    
    data = {
        "time": df['Time'].tolist(),
        "voltage": df['Voltage'].tolist()
    }
    return jsonify(data)

# Endpoint to get RUL data
@app.route('/data/<device>/rulData.csv', methods=['GET'])
def get_rul_data(device):
    file_path = os.path.join(DATA_DIRECTORY, device, 'rulData.csv')
    
    if not os.path.exists(file_path):
        return abort(404, description="RUL data file not found.")
    
    df = pd.read_csv(file_path)
    if 'DT' not in df.columns or 'RUL' not in df.columns:
        return abort(400, description="CSV file must contain 'DT' and 'RUL' columns.")
    
    data = {
        "time": df['DT'].tolist(),
        "rul": df['RUL'].tolist()
    }
    return jsonify(data)

# Endpoint to get FD data
@app.route('/data/<device>/fdData.csv', methods=['GET'])
def get_fd_data(device):
    file_path = os.path.join(DATA_DIRECTORY, device, 'rulData.csv')
    
    if not os.path.exists(file_path):
        return abort(404, description="FD data file not found.")
    
    df = pd.read_csv(file_path)
    if 'DT' not in df.columns or 'FD' not in df.columns:
        return abort(400, description="CSV file must contain 'DT' and 'FD' columns.")
    
    data = {
        "time": df['DT'].tolist(),
        "fd": df['FD'].tolist()
    }
    return jsonify(data)

# Endpoint to get SoH data
@app.route('/data/<device>/sohData.csv', methods=['GET'])
def get_soh_data(device):
    file_path = os.path.join(DATA_DIRECTORY, device, 'rulData.csv')
    
    if not os.path.exists(file_path):
        return abort(404, description="SoH data file not found.")
    
    df = pd.read_csv(file_path)
    if 'DT' not in df.columns or 'SoH' not in df.columns:
        return abort(400, description="CSV file must contain 'DT' and 'SoH' columns.")
    
    data = {
        "time": df['DT'].tolist(),
        "soh": df['SoH'].tolist()
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
