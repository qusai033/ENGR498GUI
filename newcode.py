@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Read raw CSV data from the request body
        csv_data = request.data.decode('utf-8')
        if not csv_data:
            print("Error: No data received.")  # Debug log
            return jsonify({"error": "No data received"}), 400

        # Save the received CSV data to a file in the desired folder structure
        save_path = os.path.join(DATA_DIRECTORY, "device", "voltage_log", "uploaded_file.csv")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Ensure directories exist
        with open(save_path, 'w') as f:
            f.write(csv_data)
        
        print(f"File saved to: {save_path}")  # Debug log
        return jsonify({"message": "CSV file uploaded and saved successfully."}), 200
    except Exception as e:
        print(f"Error processing CSV: {e}")  # Debug log
        return jsonify({"error": f"Error processing CSV: {e}"}), 500
