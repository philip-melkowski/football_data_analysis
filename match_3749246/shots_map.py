import json

import matplotlib.pyplot as plt
import numpy as np

# statsbomb uses yards. So will I.
pitchLengthX = 120
pitchWidthY = 80

match_id = '3749246'
home_team = 'Arsenal'
away_team = 'Manchester United'
file_name = match_id + '.json'
from pathlib import Path

with open(Path(f'../{file_name}')) as data_file:
    data = json.load(data_file)

from pandas import json_normalize

# df = json_normalize(data)

# print(df.columns.tolist())

# currently subtype is separared with dot. like type -> type.name
# change it so we have type_name instead of type.name

df = json_normalize(data=data, sep='_').assign(match_id=file_name[:-5])

print(df.columns.tolist())

shots = df.loc[df['type_name'] == 'Shot'].set_index('id')

# #drawing the pitch
from FCPython import createPitch

fig, ax = createPitch(pitchLengthX, pitchWidthY, 'yards', 'black')

# plotting the shots
# the information about shots' inital location is available in the ['location'] array
for i, shot in shots.iterrows():
    x = shot['location'][0]
    y = shot['location'][1]

    # check whether shot was a goal
    goal = shot['shot_outcome_name'] == 'Goal'
    team_name = shot['team_name']

    # size of shot circle based on xG
    circle_size = np.sqrt(shot['shot_statsbomb_xg'] * 10)

    if team_name == home_team:
        # if goal was scored with the shot set the color to red  and show scorer's name
        if goal:
            shot_circle = plt.Circle(xy=(x, pitchWidthY - y), radius=circle_size, color='red')
            plt.text(x - 20, pitchWidthY - y + 1, shot['player_name'])
        # if no goal circle colored red and slightly blended
        else:
            shot_circle = plt.Circle(xy=(x, pitchWidthY - y), radius=circle_size, color='red')
            shot_circle.set_alpha(0.5)
    # same for away team
    elif team_name == away_team:
        # if goal was scored with the shot set the color to red and show scorer's name
        if goal:
            shot_circle = plt.Circle(xy=(pitchLengthX - x, y), radius=circle_size, color='red')
            plt.text(pitchLengthX - x + 1, y - 5, shot['player_name'])
        # if no goal circle colored red and slightly blended
        else:
            shot_circle = plt.Circle(xy=(pitchLengthX - x, y), radius=circle_size, color='red')
            shot_circle.set_alpha(0.5)
    ax.add_patch(shot_circle)

plt.text(5, 75, away_team + ' shots')
plt.text(80, 75, home_team + ' shots')
plt.title('Arsenal - Manchester United Sun 28 Mar 2004 Shot Map')
plt.text(85, 5, 'Scoreline 1:1')
fig.set_size_inches(10, 7)
# fig.savefig(Path('C:/Users/Philip/Desktop/shots.pdf'))
plt.show()
