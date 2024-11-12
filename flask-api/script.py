import pandas as pd
import requests
from dotenv import load_dotenv
import os
import json
from utils import get_main_response, my_current_team_picks_ids


load_dotenv()

my_team_key = os.getenv("MY_TEAM_ID")

main_response = get_main_response()
current_team_ids = my_current_team_picks_ids()

all_premier_league_players = sorted(main_response["elements"], key= lambda x: x['id'])
my_players_details = []

for player_id in current_team_ids:
    my_players_details.append(all_premier_league_players[player_id - 1])


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
    players_with_recommendations[position].append({"my_player": current_player, "alternatives": list_of_alt[0]["alternatives"]})


def generate_for_all_players():
    for player in my_players_details:
        position = player["element_type"]
        creating_cheaper_alternative_list(player, position)
    return players_with_recommendations

