import os

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Read raw CSV data from the request body
        csv_data = request.data.decode('utf-8')
        if not csv_data:
            print("Error: No data received.")  # Debug log
            return jsonify({"error": "No data received"}), 400

        # Traverse `data` directory to find all `voltageData.csv` files
        overridden_files = []
        for root, dirs, files in os.walk(DATA_DIRECTORY):  # Recursively walk through directories
            for file in files:
                if file == 'voltageData.csv':  # Check for `voltageData.csv`
                    file_path = os.path.join(root, file)
                    
                    # Override the file content
                    with open(file_path, 'w') as f:
                        f.write(csv_data)
                    
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
