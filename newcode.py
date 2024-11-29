
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

        # Ensure Time and Voltage columns are checked for duplicates
        if 'Voltage' not in df.columns or 'Time' not in df.columns:
            print("Error: Missing 'Time' or 'Voltage' columns.")  # Debug log
            return jsonify({"error": "Missing 'Time' or 'Voltage' columns in CSV"}), 400

        # Drop duplicates based on Time and Voltage
        df = df.drop_duplicates(subset=['Voltage', 'Time'])

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
