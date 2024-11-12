from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from script import generate_for_all_players

load_dotenv()

app = Flask(__name__)

my_team_key = os.getenv("MY_TEAM_ID")

@app.route(f"/api/team/{my_team_key}/alternatives", methods = ["GET"])
def info():
    information = generate_for_all_players()
    return jsonify(information)

if __name__ == "__main__":
    # Make sure to change debug to false when pushing to prod
    app.run(debug=True)

print(generate_for_all_players())