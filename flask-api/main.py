from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from script import parse_to_api
import json
import requests

# Load environment variables
load_dotenv()

# Flask app initialization
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

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
        information = parse_to_api()  
        data = json.loads(information)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route(f"/api/player/<int:player_id>/altplayer/<int:altPlayer_id>", methods=["GET"])
def get_player_data(player_id, altPlayer_id):
    try:
        url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
        url2 = f"https://fantasy.premierleague.com/api/element-summary/{altPlayer_id}/"
        response = requests.get(url)
        response2 = requests.get(url2)
        response.raise_for_status()
        response2.raise_for_status()

        final_response = {player_id: response.json(), altPlayer_id: response2.json()}
        return jsonify(final_response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Set debug=False for production
    app.run(debug=True)
