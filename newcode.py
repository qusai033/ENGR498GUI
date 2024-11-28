from flask import Flask, jsonify, request, abort
import os

app = Flask(__name__)

# Path to the directory containing device folders
DATA_DIRECTORY = './data/device/voltage_log'  # Update to match your directory structure
COUNTER_FILE = './file_counter.txt'  # File to store the counter

# Ensure directories and counter file exist
os.makedirs(DATA_DIRECTORY, exist_ok=True)
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
        filename = f"file_{file_counter}.csv"

        # Save the received CSV data to the desired folder
        save_path = os.path.join(DATA_DIRECTORY, filename)
        with open(save_path, 'w') as f:
            f.write(csv_data)

        print(f"File saved to: {save_path}")  # Debug log
        return jsonify({"message": f"File '{filename}' uploaded and saved successfully.", "file_number": file_counter}), 200
    except Exception as e:
        print(f"Error processing CSV: {e}")  # Debug log
        return jsonify({"error": f"Error processing CSV: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
