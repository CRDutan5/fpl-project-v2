from utils import get_main_response, my_current_team_picks_ids, determine_gameweek_for_picks
import datetime
import sys
# Main api response
main_response = get_main_response()
# My current team ids
current_team_ids = my_current_team_picks_ids()

# Current gameweek
current_gameweek = determine_gameweek_for_picks()

# Stores all the players in the premier league
all_premier_league_players = sorted(main_response["elements"], key= lambda x: x['id'])

# Stores ONLY my players information in the array my_player_details
my_players_details = []
for player_id in current_team_ids:
    my_players_details.append(all_premier_league_players[player_id - 1])

# Main structure of json to seperate my players based on position
players_with_recommendations = {
    "goalkeepers": [],
    "defenders": [],
    "midfielders": [],
    "forwards": []
}

# Need hashmap to compare the position number and send it to the appropriate array in players_with_recommendations
position_hashmap = {1: "goalkeepers", 2: "defenders", 3: "midfielders", 4: "forwards"}

# Takes in a player and position number, generates a list of cheaper alternatives for that player
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

# Uses the creating_cheaper_alternative_list function and generates a list of recommendations for all my current players
def generate_for_all_players():
    for player in my_players_details:
        position = player["element_type"]
        creating_cheaper_alternative_list(player, position)
    return players_with_recommendations


def generate_writing(position, file_path):    
    with open(file_path, 'a') as f:
        for player in players_with_recommendations[position]:
            current_player = player["my_player"]
            f.write(f"Current Player: {current_player['first_name']} {current_player['second_name']}\n")
            
            if len(player["alternatives"]) != 0:
                for alt_player in player["alternatives"]:
                    f.write(f'We recommend {alt_player["first_name"]} {alt_player["second_name"]} from Team: {alt_player["team"]}\n')
            else:
                f.write("No cheaper alternatives\n")
            
            f.write("____________________________________________________\n")


try :
    generate_for_all_players()
    generate_writing("goalkeepers", f"Gameweek-{current_gameweek}.txt")
    generate_writing("defenders", f"Gameweek-{current_gameweek}.txt")
    generate_writing("midfielders", f"Gameweek-{current_gameweek}.txt")
    generate_writing("forwards", f"Gameweek-{current_gameweek}.txt")
    current_time = datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S")
    print(f'[{current_time}] Successfully executed script for Gameweek: {current_gameweek}')

except Exception as e:
    current_time = datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S")
    print(f'[{current_time}] Error executing script: {str(e)}', file=sys.stderr)
    raise e


