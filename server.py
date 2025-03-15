from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allows frontend to communicate with backend

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No file selected"}), 400

    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({"message": f"File {file.filename} uploaded successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
