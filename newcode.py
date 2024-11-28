from flask import Flask, jsonify, render_template, request, abort
import pandas as pd
import os

app = Flask(__name__)

# Path to the directory containing device folders
DATA_DIRECTORY = '../data'  # Relative path to the data folder

@app.route('/')
def index():
    return render_template('index.html')



# Upload file route
@app.route('/upload', methods=['POST'])
def upload():
    print("Received a connection")
    # Process file here
    return "File received", 200

    

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
@app.route('/data/<device>/voltageData.csv', methods=['GET'])
def get_voltage_data(device):
    file_path = os.path.join(DATA_DIRECTORY, device, 'voltageData.csv')
    
    if not os.path.exists(file_path):
        return abort(404, description="Voltage data file not found.")
    
    # Load the CSV data into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Check if the necessary columns exist in the CSV
    if 'Time' not in df.columns or 'Voltage' not in df.columns:
        return abort(400, description="CSV file must contain 'Time' and 'Voltage' columns.")
    
    # Convert the DataFrame to a dictionary suitable for JSON
    data = {
        "time": df['Time'].tolist(),
        "voltage": df['Voltage'].tolist()
    }
    
    return jsonify(data)

@app.route('/data/<device>/rulData.csv', methods=['GET'])
def get_rul_fd_soh_data(device):
    file_path = os.path.join(DATA_DIRECTORY, device, 'rulData.csv')
    
    if not os.path.exists(file_path):
        return abort(404, description="RUL data file not found.")
    
    try:
        df = pd.read_csv(file_path)
        
        # Ensure all required columns exist
        required_columns = ['DT', 'RUL', 'PH', 'FD', 'SOH']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return abort(400, description=f"Missing columns: {', '.join(missing_columns)}")
        
        # Prepare JSON response
        data = {
            "time": df['DT'].tolist(),
            "rul": df['RUL'].tolist(),
            "ph": df['PH'].tolist(),
            "fd": df['FD'].tolist(),
            "eol": df['EOL'].tolist(),
            "bd": df['BD'].tolist(),
            "soh": df['SOH'].tolist()
        }
        return jsonify(data)
    except Exception as e:
        print("Error:", e)  # Debug error
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
