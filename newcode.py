from flask import Flask, jsonify, render_template, request, abort
import pandas as pd
import os

app = Flask(__name__)


# Path to the directory containing device folders
DATA_DIRECTORY = '../data'  # Relative path to the data folder
# Upload file route
# Path to the directory containing device folders
# Path to the directory containing device folders
UPLOAD_DATA_DIRECTORY = './data/uploads/voltage_log'  # Update to match your directory structure
COUNTER_FILE_DIRECTORY = './data/uploads'  # File to store the counter

COUNTER_FILE = os.path.join(COUNTER_FILE_DIRECTORY, 'file_voltage_counter.txt')

# Ensure directories and counter file exist
os.makedirs(UPLOAD_DATA_DIRECTORY, exist_ok=True)
os.makedirs(COUNTER_FILE_DIRECTORY, exist_ok=True)

if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, 'w') as f:
        f.write('0')  # Initialize the counter to 0


# Function to get the current counter value
def get_file_counter():
    with open(COUNTER_FILE, 'r') as f:
        return int(f.read().strip())


# Function to increment and save the counter
def increment_file_counter():
    counter = get_file_counter() + 1
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(counter))
    return counter



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Read raw CSV data from the request body
        csv_data = request.data.decode('utf-8')
        if not csv_data:
            print("Error: No data received.")  # Debug log
            return jsonify({"error": "No data received"}), 400

        # Increment the file counter and generate a unique filename
        file_counter = increment_file_counter()
        filename = f"voltageDecay_{file_counter}.csv"

        # Save the received CSV data to the desired folder
        save_path = os.path.join(UPLOAD_DATA_DIRECTORY, filename)
        with open(save_path, 'w') as f:
            f.write(csv_data)

        print(f"File saved to: {save_path}")  # Debug log
        return jsonify({"message": f"File '{filename}' uploaded and saved successfully.", "file_number": file_counter}), 200
    except Exception as e:
        print(f"Error processing CSV: {e}")  # Debug log
        return jsonify({"error": f"Error processing CSV: {e}"}), 500



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
