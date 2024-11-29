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

        # Also override or update the master file (voltageData.csv) in DATA_DIRECTORY
        master_file_path = os.path.join(DATA_DIRECTORY, 'voltageData.csv')
        with open(master_file_path, 'w') as f:
            f.write(csv_data)

        print(f"Master file updated: {master_file_path}")  # Debug log

        return jsonify({
            "message": f"File '{unique_filename}' uploaded successfully and master file updated.",
            "file_number": file_counter
        }), 200

    except Exception as e:
        print(f"Error processing CSV: {e}")  # Debug log
        return jsonify({"error": f"Error processing CSV: {e}"}), 500
