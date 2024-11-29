@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Read raw CSV data from the request body
        csv_data = request.data.decode('utf-8')
        if not csv_data:
            print("Error: No data received.")  # Debug log
            return jsonify({"error": "No data received"}), 400

        # Convert CSV data into a Pandas DataFrame
        from io import StringIO
        csv_stream = StringIO(csv_data)
        df = pd.read_csv(csv_stream)

        # Remove duplicates
        df = df.drop_duplicates()

        # Save the cleaned, unique data to the uploads directory with a unique name
        file_counter = increment_file_counter()
        unique_filename = f"voltageDecay_{file_counter}.csv"
        save_path = os.path.join(UPLOAD_DATA_DIRECTORY, unique_filename)
        df.to_csv(save_path, index=False)
        print(f"Unique data saved to: {save_path}")  # Debug log

        # Override all `voltageData.csv` files in `data` directory
        overridden_files = []
        for root, dirs, files in os.walk(DATA_DIRECTORY):
            for file in files:
                if file == 'voltageData.csv':
                    file_path = os.path.join(root, file)
                    df.to_csv(file_path, index=False)  # Save unique data
                    overridden_files.append(file_path)

        if not overridden_files:
            return jsonify({"message": "No voltageData.csv files found to override."}), 404

        print(f"Overridden files: {overridden_files}")  # Debug log
        return jsonify({
            "message": f"Uploaded data saved and overridden {len(overridden_files)} voltageData.csv files successfully.",
            "overridden_files": overridden_files
        }), 200
    except Exception as e:
        print(f"Error processing CSV: {e}")  # Debug log
        return jsonify({"error": f"Error processing CSV: {e}"}), 500
