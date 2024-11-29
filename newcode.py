import pandas as pd

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
        unique_filename = f"voltageDecay_{file_counter}.csv"

        # Save the uniquely named file in the uploads directory
        save_path = os.path.join(UPLOAD_DATA_DIRECTORY, unique_filename)
        with open(save_path, 'w') as f:
            f.write(csv_data)

        print(f"File saved to: {save_path}")  # Debug log

        # Convert CSV data into a DataFrame for normalization
        try:
            df = pd.read_csv(save_path)
            # Rename columns for consistency
            if 'Time(s)' in df.columns:
                df.rename(columns={'Time(s)': 'Time'}, inplace=True)
            if 'Voltage' not in df.columns:
                return jsonify({"error": "CSV must contain 'Voltage' column."}), 400
        except Exception as e:
            print(f"Error reading or processing CSV: {e}")
            return jsonify({"error": f"Error processing CSV: {e}"}), 400

        # Traverse `data` directory to find and override `voltageData.csv` files
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
