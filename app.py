from flask import Flask, jsonify, send_from_directory, request, abort
import pandas as pd
import os

app = Flask(__name__)

# Path to the directory containing CSV files
DATA_DIRECTORY = './data'

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/get_health_data', methods=['GET'])
def get_health_data():
    # Specify the CSV file you want to read from the folder
    csv_file = os.path.join(DATA_DIRECTORY, 'health_data.csv')
    
    # Check if the file exists
    if not os.path.exists(csv_file):
        return abort(404, description="CSV file not found.")
    
    # Load the CSV data into a pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Convert the DataFrame to a dictionary suitable for JSON
    data = {
        "timestamps": df['Timestamp'].tolist(),
        "health_metric_1": df['HealthMetric1'].tolist(),
        "health_metric_2": df['HealthMetric2'].tolist()
    }
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
