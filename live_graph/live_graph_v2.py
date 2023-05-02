import json

import requests
import matplotlib; matplotlib.use("TkAgg")


import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import collections

player_list = ["Thomas", "Hugues", "Lucas", "Paul", "Laurent"]

player_dict = {}
for player in player_list:
    player_dict[player] = collections.deque([0]*60)


def get_new_info(i):
    response = requests.get("http://gubendo.pythonanywhere.com/get_height/")
    data = response.json()

    # clear axis
    ax1.cla()

    for player in player_list:
        player_dict[player].popleft()
        player_dict[player].append([item[1] for item in data if item[0] == player][0])

        progr, = ax1.plot(player_dict[player], label=player)
        ax1.scatter(len(player_dict[player]) - 1, player_dict[player][-1], color=progr.get_color())
        ax1.text(len(player_dict[player]) - 1, player_dict[player][-1] + 3, f"{player_dict[player][-1]}", fontsize=20, color=progr.get_color())
        plt.hlines([item[2] for item in data if item[0] == player][0], xmin=0, xmax=60, linestyles="dotted", color=progr.get_color())
        ax1.text(0, [item[2] for item in data if item[0] == player][0] + 3,
             f"Record de {player}: {[item[2] for item in data if item[0] == player][0]}",
             fontsize=15, color=progr.get_color())

    legend = plt.legend(fontsize=20)

    return legend


# define and adjust figure
fig = plt.figure(figsize=(18, 12), facecolor="white")
ax1 = plt.subplot(111) #221
ax1.set_facecolor('white')

ani = FuncAnimation(fig, get_new_info, interval=1000)  # Refreshes every X ms
plt.legend()
plt.show()

