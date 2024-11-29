@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Step 1: Receive CSV data from the Arduino
        csv_data = request.data.decode('utf-8')
        if not csv_data:
            print("Error: No data received.")  # Debug log
            return jsonify({"error": "No data received"}), 400

        # Step 2: Convert to Pandas DataFrame
        csv_stream = StringIO(csv_data)
        df = pd.read_csv(csv_stream)

        # Step 3: Deduplicate the data (excluding the first row)
        first_row = df.iloc[:1]  # Keep the first row separately
        remaining_data = df.iloc[1:]  # All data except the first row
        deduplicated_data = remaining_data.drop_duplicates(subset=['Time', 'Voltage'])  # Remove duplicates
        deduplicated_df = pd.concat([first_row, deduplicated_data], ignore_index=True)  # Combine back

        # Step 4: Save the deduplicated file to the uploads directory
        file_counter = increment_file_counter()
        unique_filename = f"voltageDecay_{file_counter}.csv"
        save_path = os.path.join(UPLOAD_DATA_DIRECTORY, unique_filename)
        deduplicated_df.to_csv(save_path, index=False)
        print(f"Unique data saved to: {save_path}")  # Debug log

        # Step 5: Override all `voltageData.csv` files in the `data` directory
        overridden_files = []
        for root, dirs, files in os.walk(DATA_DIRECTORY):
            for file in files:
                if file == 'voltageData.csv':
                    file_path = os.path.join(root, file)
                    deduplicated_df.to_csv(file_path, index=False)
                    overridden_files.append(file_path)

        # Step 6: Return response
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
