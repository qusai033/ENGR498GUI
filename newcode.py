from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Directory where files will be saved
SAVE_FOLDER = 'data/received_files'
os.makedirs(SAVE_FOLDER, exist_ok=True)  # Ensure the folder exists

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print("Error: No file part in the request.")  # Log the error
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        print("Error: No file selected.")  # Log the error
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
