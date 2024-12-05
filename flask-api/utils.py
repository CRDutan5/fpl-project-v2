import requests
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

my_team_key = os.getenv("MY_TEAM_ID")

# Main api response
def get_main_response():
    main_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    main_response = requests.get(main_url).json()
    return main_response

# function to grab prev gameweek to look at picks
def determine_gameweek_for_picks():
    main_response = get_main_response()
    gameweeks = main_response["events"]
    for i in range(len(gameweeks)):
        if gameweeks[i]["is_current"] == True:
            return gameweeks[i]["id"]

# Grabs my players ids for the week
def my_current_team_picks_ids():
    current_gameweek = determine_gameweek_for_picks()
    url = (f"https://fantasy.premierleague.com/api/entry/{my_team_key}/event/{current_gameweek}/picks/")
    res = requests.get(url).json()
    current_team_df = pd.DataFrame(res["picks"])
    current_team_ids = current_team_df["element"].tolist()
    return current_team_ids

