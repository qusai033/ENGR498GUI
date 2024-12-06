from flask import Flask, jsonify, render_template, request, abort
import pandas as pd
import os
from io import StringIO


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
        

        # Convert CSV data into a Pandas DataFrame

        csv_stream = StringIO(csv_data)
        df = pd.read_csv(csv_stream)


        df.columns = df.columns.str.strip()

        # Ensure Time and Voltage columns are checked for duplicates
        if 'Voltage' not in df.columns or 'Time' not in df.columns:
            print("Error: Missing 'Time' or 'Voltage' columns.")  # Debug log
            return jsonify({"error": "Missing 'Time' or 'Voltage' columns in CSV"}), 400
        

        original_length = len(df)


        # Drop duplicates based on Time and Voltage
        df = df.drop_duplicates(subset=['Voltage', 'Time'])

        new_lenth = len(df)

        print(f"remove {original_length - new_lenth} duplicate rows.")

        # Increment the file counter and generate a unique filename
        file_counter = increment_file_counter()
        unique_filename = f"voltageDecay_{file_counter}.csv"

        # Save the uniquely named file in the uploads directory
        save_path = os.path.join(UPLOAD_DATA_DIRECTORY, unique_filename)
        df.to_csv(save_path, index=False)

        print(f"File saved to: {save_path}")  # Debug log


        # Traverse `data` directory to find all `voltageData.csv` files
        overridden_files = []
        for root, dirs, files in os.walk(DATA_DIRECTORY):  # Recursively walk through directories
            for file in files:
                if file == 'voltageData.csv':  # Check for `voltageData.csv`
                    file_path = os.path.join(root, file)
                    
                    # Override the file content with normalized data
                    df.to_csv(file_path, index=False)  # Save normalized DataFrame
                    overridden_files.append(file_path)
                    

        if not overridden_files:
            return jsonify({"message": "No voltageData.csv files found to override."}), 404

        print(f"Overridden files: {overridden_files}")  # Debug log
        return jsonify({
            "message": f"Overridden {len(overridden_files)} voltageData.csv files successfully.",
            "overridden_files": overridden_files
        }), 200
    

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
            "eol": df['EOL'].tolist() if 'EOL' in df.columns else [0] * len(df),
            "bd": df['BD'].tolist() if 'BD' in df.columns else [0] * len(df),
            "soh": df['SOH'].tolist()
        }
        return jsonify(data)
    except Exception as e:
        print("Error:", e)  # Debug error
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



#Import libraries
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import os
import matplotlib.pyplot as plt

def process_decay_data(baseline_file, new_file):

    baseCurve = pd.read_csv(baseline_file)    
    baseCurve['Voltage'] = baseCurve['Voltage'].replace(0, 0.01)

    newCurve = pd.read_csv(new_file)
    newCurve['Voltage'] = newCurve['Voltage'].replace(0, 0.01)

    baseCurve['Vinv'] = 1 / baseCurve['Voltage']
    newCurve['Vinv'] = 1 / newCurve['Voltage']

    #Interpolate data
    f1 = interp1d(newCurve['Voltage'], newCurve['Time'], kind = 'linear', fill_value='extrapolate')
    f2 = interp1d(baseCurve['Voltage'], newCurve['Time'], kind = 'linear', fill_value='extrapolate')

    #Interpolate inverse data
    f1Inv = interp1d(newCurve['Vinv'], newCurve['Time'], kind = 'linear', fill_value='extrapolate')
    f2Inv = interp1d(baseCurve['Vinv'], newCurve['Time'], kind = 'linear', fill_value='extrapolate')
    
    #Find common voltages
    commonVolts = np.linspace(
        min(newCurve['Voltage'].min(), baseCurve['Voltage'].min()),
        max(newCurve['Voltage'].max(), baseCurve['Voltage'].max()),
        500
    )

    #find common inverse voltages
    commonVoltsInv = np.linspace(
        min(newCurve['Vinv'].min(), baseCurve['Vinv'].min()), 
        max(newCurve['Vinv'].max(), baseCurve['Vinv'].max()),
        500
    )

    interpolatedTime1 = f1(commonVolts)
    interpolatedTime2 = f2(commonVolts)

    interpolatedInvTime1 = f1Inv(commonVoltsInv)
    interpolatedInvTime2 = f2Inv(commonVoltsInv)

    timeDifference = interpolatedTime2 - interpolatedTime1
    timeDifferenceInv = interpolatedInvTime2 - interpolatedInvTime1

    plt.plot(timeDifferenceInv, commonVoltsInv, label= 'Interpolated Time Difference Between Voltage Values')
    plt.xlabel('Time Difference (uS)')
    plt.ylabel('Volts (V)')
    plt.show  

    #export the differences of the files to a .csv file
    differences_df = pd.DataFrame({
        "TimeDifferences": timeDifference,
        "Voltages":commonVolts
    })
    differences_df.to_csv('timeDifferences.csv')

    differences_df = pd.DataFrame({
        "TimeDifferencesInv": timeDifferenceInv,
        "VoltagesInv":commonVoltsInv
    })
    differences_df.to_csv('timeDifferencesInv.csv')

#Define the baseline file. The baseline will be the first reading
baseline_file = "data2(Good Cap).csv"

#Define the new file that just came in. Need to add code that switches this whenever a new file comes in.
new_file = "data1(Bad Cap).csv"

process_decay_data(baseline_file, new_file)
