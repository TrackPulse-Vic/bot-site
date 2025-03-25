from flask import Flask, send_file, abort, Response
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={"/csv/*": {"origins": "*"}})  # Allow all origins for /csv/*

CSV_DIR = "D:\\Billy\\Douments\\Self made programs\\Melbourne-transport-discord-bot\\utils\\trainlogger\\userdata"
    
@app.route('/csv/<filename>')
def serve_csv(filename):
    file_path = os.path.join(CSV_DIR, filename)
    print(f"Requested file: {filename}")
    print(f"Full path: {file_path}")
    print(f"Path exists: {os.path.exists(file_path)}")
    print(f"Is CSV: {file_path.endswith('.csv')}")
    print(f"Files in directory: {os.listdir(CSV_DIR)}")
    
    if os.path.exists(file_path) and file_path.endswith('.csv'):
        response = send_file(file_path, mimetype='text/csv')
        response.headers['Access-Control-Allow-Origin'] = '*'  # Manual header as fallback
        return response
    else:
        abort(404, description=f"File not found or not a CSV at {file_path}")

# Test route to check CORS
@app.route('/test')
def test_cors():
    return Response("CORS Test", mimetype='text/plain', headers={'Access-Control-Allow-Origin': '*'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)