from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from script import parse_to_api
import json

# Load environment variables
load_dotenv()

# Flask app initialization
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Retrieve team key from environment variables
my_team_key = os.getenv("MY_TEAM_ID")
if not my_team_key:
    raise ValueError("MY_TEAM_ID is not set in the environment variables")

@app.route(f"/api/team/{my_team_key}/alternatives", methods=["GET"])
def get_team_alternatives():
    """
    Endpoint to get team alternatives.
    This calls the `parse_to_api` function dynamically to ensure data is up-to-date.
    """
    try:
        information = parse_to_api()  # Get fresh data
        # Ensure the JSON string is parsed into a Python dictionary before jsonify
        data = json.loads(information)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Set debug=False for production
    app.run(debug=True)
