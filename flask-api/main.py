from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from script import generate_for_all_players


load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

my_team_key = os.getenv("MY_TEAM_ID")

information = generate_for_all_players()

@app.route(f"/api/team/{my_team_key}/alternatives", methods = ["GET"])
def info():
    return jsonify(information)

if __name__ == "__main__":
    # Make sure to change debug to false when pushing to prod
    app.run(debug=True)