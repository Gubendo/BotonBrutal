import json

import requests
import time

response_init = requests.get("http://gubendo.pythonanywhere.com/get_height/")
data_init = response_init.json()

players = [item[0] for item in data_init]
pos_dict = {}
best_dict = {}

pos_live = [0]*10

iter = 1
iter_last_saved = 0
for player in players:
    pos_dict[player] = [item[1] for item in data_init if item[0] == player]
    best_dict[player] = [item[2] for item in data_init if item[0] == player]

while True:
    response = requests.get("http://gubendo.pythonanywhere.com/get_height/")
    data = response.json()

    new_players = list(set([item[0] for item in data]) - set(players))

    if len(new_players) > 0:
        print(f"New players {', '.join(new_players)} have entered the game !")

        for player in players:
            pos_dict[player] = [0]*iter
            best_dict[player] = [0]*iter

    for player in players:
        pos_dict[player].append([item[1] for item in data if item[0] == player][0])
        best_dict[player].append([item[2] for item in data if item[0] == player][0])

    iter += 1

    if (iter_last_saved == 0) or (iter > iter_last_saved + 30):
        out_file = open("pos_log.json", "w")
        json.dump(pos_dict, out_file, indent=6)
        out_file.close()

        out_file = open("best_log.json", "w")
        json.dump(best_dict, out_file, indent=6)
        out_file.close()

        print("saved logs")
        iter_last_saved = iter

    time.sleep(2)

