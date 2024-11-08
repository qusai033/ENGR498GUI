# Upload file route
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Get the uploaded file content from the request
        file_content = request.data  # This will capture the raw data sent by the Arduino

        # Save the file to the specified path
        file_path = os.path.join(UPLOAD_FOLDER, "uploaded_file.csv")
        with open(file_path, "wb") as f:  # Write the file content in binary mode
            f.write(file_content)
        
        return "File uploaded successfully", 200
    except Exception as e:
        return str(e), 500
