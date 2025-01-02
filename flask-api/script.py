from utils import get_main_response, my_current_team_picks_ids, determine_gameweek_for_picks, send_email
import datetime
import sys
import json

main_response = get_main_response()
all_players_response = sorted(main_response["elements"], key=lambda x: x["now_cost"])
current_gameweek = determine_gameweek_for_picks()

my_player_ids = my_current_team_picks_ids()

class Player:
    def __init__(self, id, data, alts = None):
        self.id = id
        self.data = data
        self.alts = alts
        self.next = None

class PlayerList:
    def __init__(self):
        self.head = Player(None, None)
        self.tail = Player(None, None)
        self.head.next = self.tail
    
    def add_player(self, player_node):
        next_node = self.head.next
        self.head.next = player_node
        player_node.next = next_node

    def display(self):
        i = 1
        curr = self.head.next
        while curr != self.tail:
            print(i, curr.id, curr.data["first_name"], curr.data["second_name"], curr.data["now_cost"] ,curr.alts)
            curr = curr.next
            i+=1

    def remove_player(self, player_node, prev_player_node):
        prev_player_node.next = player_node.next
        return player_node

my_team = PlayerList()
available_players = PlayerList()
    
for player in all_players_response:
    if player["id"] in my_player_ids:
        new_player = Player(player["id"], player, [])
        my_team.add_player(new_player)

    else:
        new_player = Player(player["id"], player)
        available_players.add_player(new_player)

def generate_cheaper_alt():
    curr = my_team.head.next
    while curr and curr != my_team.tail:
        curr2 = available_players.head.next
        curr2_prev = available_players.head
        while curr2 and curr2 != available_players.tail and len(curr.alts) < 3:
            if (float(curr.data["form"]) <= float(curr2.data["form"]) and 
                curr.data["element_type"] == curr2.data["element_type"] and 
                curr.data["now_cost"] >= curr2.data["now_cost"]):
                alt_player = available_players.remove_player(curr2, curr2_prev)
                curr.alts.append(alt_player)
            else:
                curr2_prev = curr2
            curr2 = curr2.next
        curr = curr.next

def generate_writing(file_path):
    with open(file_path, 'a') as f:
        curr = my_team.head.next
        while curr != my_team.tail:
            current_player = curr.data
            f.write(f"{current_player['first_name']} {current_player['second_name']} Recommendations:\n")    
            if len(curr.alts) > 0:
                for alt_player in curr.alts:
                    f.write(f"Alt: {alt_player.data['first_name']} {alt_player.data['second_name']}\n")
            else:
                f.write("No cheaper alternatives!\n")
            f.write("---------------------------------------\n")
            curr = curr.next

def handle_alts(player_alts):
    list_alts = []
    if len(player_alts) == 0:
        return list_alts
    
    for player in player_alts:
        list_alts.append({
        "id": player.id,
        "data": player.data,
    })
    return list_alts
    

def linked_list_to_json(player_list):
    players = []
    curr = player_list.head.next

    while curr != player_list.tail:
        players.append({
            "id": curr.id,
            "data": curr.data,
            "alts": handle_alts(curr.alts)
        })
        curr = curr.next
    return json.dumps({"team": players}, indent= 4)

def parse_to_api():
    generate_cheaper_alt()
    json_data = linked_list_to_json(my_team)
    return json_data


# try:
#     generate_cheaper_alt()
#     generate_writing(f"Gameweek-{current_gameweek}.txt")
#     print("Sending email...")
#     send_email(current_gameweek)
#     print("Email sent.")
#     current_time = datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S")
#     print(f'[{current_time}] Successfully executed script for Gameweek: {current_gameweek}')

# except Exception as e:
#     current_time = datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S")
#     print(f'[{current_time}] Error executing script: {str(e)}', file=sys.stderr)
#     raise e