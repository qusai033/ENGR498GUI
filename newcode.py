@app.route('/upload', methods=['POST'])
def upload_file():
    print("Received upload request")  # Log request received
    
    if 'file' not in request.files:
        print("Error: No file part in the request.")  # Log error
        print("Request data:", request.data)  # Log raw request data
        print("Request headers:", request.headers)  # Log headers
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    print("File received:", file.filename)  # Log file name
    
    if file.filename == '':
        print("Error: No file selected.")  # Log error
        return jsonify({"error": "No file selected"}), 400

    # Save the file to the save folder
    try:
        save_path = os.path.join(SAVE_FOLDER, file.filename)
        file.save(save_path)
        print(f"File '{file.filename}' saved to '{save_path}'")  # Log success
        return jsonify({"message": f"File '{file.filename}' uploaded successfully."}), 200
    except Exception as e:
        print(f"Error: Failed to save file: {str(e)}")  # Log the error
        return jsonify({"error": f"Failed to save file: {str(e)}"}), 500
