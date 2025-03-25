from flask import Flask, request, send_file, abort, make_response
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={"/csv/*": {"origins": "*"}})  # Allow all origins

CSV_DIR = "D:\\Billy\Douments\\Self made programs\\Melbourne-transport-discord-bot\\utils\\trainlogger\\userdata"

@app.route('/csv/<filename>', methods=['GET', 'OPTIONS'])
def serve_csv(filename):
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Accept, ngrok-skip-browser-warning'
        print("Handled OPTIONS preflight request")
        return response

    file_path = os.path.join(CSV_DIR, filename)
    print(f"Requested file: {filename}")
    print(f"Full path: {file_path}")
    print(f"Path exists: {os.path.exists(file_path)}")
    print(f"Is CSV: {file_path.endswith('.csv')}")
    print(f"Files in directory: {os.listdir(CSV_DIR)}")
    
    if os.path.exists(file_path) and file_path.endswith('.csv'):
        response = send_file(file_path, mimetype='text/csv')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        response = make_response(f"File not found or not a CSV at {file_path}", 404)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)