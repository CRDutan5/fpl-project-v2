from utils import get_main_response, my_current_team_picks_ids, determine_gameweek_for_picks, send_email

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

    while curr != my_team.tail:
        curr2 = available_players.head.next
        curr2_prev = available_players.head
        # Future Referrence: Make sure data types are compared correctly. Form was a string but i had to parse to float.
        while curr2 != available_players.tail and len(curr.alts) < 3:
            if (float(curr.data["form"]) <= float(curr2.data["form"]) and 
                curr.data["element_type"] == curr2.data["element_type"] and 
                curr.data["now_cost"] >= curr2.data["now_cost"]):
                alt_player = available_players.remove_player(curr2, curr2_prev)
                curr.alts.append(alt_player)
            curr2_prev = curr2
            curr2 = curr2.next
        curr = curr.next

generate_cheaper_alt()

# my_team.display()



def generate_writing():

    curr = my_team.head.next
    while curr != my_team.tail:
        current_player = curr.data
        print(f"{current_player["first_name"]} {current_player["second_name"]} Recommendations:")    
        if len(curr.alts) > 0:
            for alt_player in curr.alts:
                print(f"Alt: {alt_player.data["first_name"]} {alt_player.data["second_name"]}")
        else:
            print("No recommendations!")
        print("---------------------------------------")
        curr = curr.next

generate_writing()


# try :
#     generate_for_all_players()
#     generate_writing("goalkeepers", f"Gameweek-{current_gameweek}.txt")
#     generate_writing("defenders", f"Gameweek-{current_gameweek}.txt")
#     generate_writing("midfielders", f"Gameweek-{current_gameweek}.txt")
#     generate_writing("forwards", f"Gameweek-{current_gameweek}.txt")
#     send_email(current_gameweek)
#     current_time = datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S")
#     print(f'[{current_time}] Successfully executed script for Gameweek: {current_gameweek}')

# except Exception as e:
#     current_time = datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S")
#     print(f'[{current_time}] Error executing script: {str(e)}', file=sys.stderr)
#     raise e


