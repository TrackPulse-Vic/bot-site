from flask import Flask, request, send_file, make_response, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import requests
from urllib.parse import urlencode

app = Flask(__name__)
CORS(app, resources={
    "/csv/*": {"origins": "*"},
    "/auth/discord": {"origins": "*"}
})

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Configuration
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_USER_URL = "https://discord.com/api/users/@me"

from dotenv import load_dotenv
load_dotenv()
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
CSV_DIR = os.getenv("CSV_DIR")

@app.route('/csv/<filename>', methods=['GET', 'OPTIONS'])
@limiter.limit("100/day")
def serve_csv(filename):
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Accept, ngrok-skip-browser-warning'
        print("Handled OPTIONS preflight request for /csv")
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

@app.route('/auth/discord', methods=['POST', 'OPTIONS'])
@limiter.limit("50/day;10/hour")
def discord_auth():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        print("Handled OPTIONS preflight request for /auth/discord")
        return response

    data = request.get_json()
    if not data or 'code' not in data or 'redirect_uri' not in data:
        return jsonify({"error": "Missing code or redirect_uri"}), 400

    code = data['code']
    redirect_uri = data['redirect_uri']

    token_payload = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }

    try:
        token_response = requests.post(DISCORD_TOKEN_URL, data=token_payload, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        token_response.raise_for_status()
        token_data = token_response.json()
        access_token = token_data.get('access_token')

        if not access_token:
            return jsonify({"error": "Failed to obtain access token"}), 500

        user_response = requests.get(DISCORD_USER_URL, headers={
            'Authorization': f'Bearer {access_token}'
        })
        user_response.raise_for_status()
        user_data = user_response.json()
        username = user_data.get('username')

        if not username:
            return jsonify({"error": "Failed to obtain username"}), 500

        response = jsonify({"access_token": access_token, "username": username})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except requests.RequestException as e:
        print(f"Error during Discord auth: {e}")
        return jsonify({"error": "Authentication failed"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=False)