import pandas as pd
import requests
from dotenv import load_dotenv
import os
import json


load_dotenv()

my_team_key = os.getenv("MY_TEAM_ID")

url = (f"https://fantasy.premierleague.com/api/entry/{my_team_key}/event/8/picks/")
res = requests.get(url).json()

current_team_df = pd.DataFrame(res["picks"])
current_team_ids = current_team_df["element"].tolist()
# print(current_team_ids)

main_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
main_response = requests.get(main_url).json()

all_premier_league_players = sorted(main_response["elements"], key= lambda x: x['id'])
my_players_details = []

for player_id in current_team_ids:
    my_players_details.append(all_premier_league_players[player_id - 1])

my_players_df = pd.DataFrame(my_players_details)


players_with_recommendations = {
    "goalkeepers": [],
    "defenders": [],
    "midfielders": [],
    "forwards": []
}

position_hashmap = {1: "goalkeepers", 2: "defenders", 3: "midfielders", 4: "forwards"}

def creating_cheaper_alternative_list(current_player, element_type):
    list_of_alt = [{"my_player": current_player, "alternatives": []}]
    
    for player in all_premier_league_players:
        if (
            player["id"] != current_player["id"]
            and current_player["now_cost"] >= player["now_cost"]
            and player["form"] >= current_player["form"]
            and player["element_type"] == element_type
        ):
            list_of_alt[0]["alternatives"].append(player)

    list_of_alt[0]["alternatives"].sort(key=lambda x: x["form"], reverse=True)
    list_of_alt[0]["alternatives"] = list_of_alt[0]["alternatives"][:2]
    
    position = position_hashmap[element_type]
    players_with_recommendations[position].append(list_of_alt)

def generate_for_all_players():
    for player in my_players_details:
        position = player["element_type"]
        creating_cheaper_alternative_list(player, position)

print(generate_for_all_players())

# print(json.dumps(players_with_recommendations, indent=4))
