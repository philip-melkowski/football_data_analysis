# shows Thiery Henry's all passes during the game


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

df = json_normalize(data=data, sep='_').assign(match_id=file_name[:-5])

print(df.columns.tolist())

# obtaining Thierry Henry's passes

passes = df[np.logical_and(df['type_name'] == 'Pass', df['player_name'] == 'Thierry Henry')]
print(passes.columns.tolist())
print(len(passes))  # Thierry Henry made 26 passes that game.

# drawing the pitch
from FCPython import createPitch

fig, ax = createPitch(pitchLengthX, pitchWidthY, 'yards', 'black')

# plotting the passes
for i, the_pass in passes.iterrows():
    x = the_pass['location'][0]
    y = the_pass['location'][1]
    # circle for starting location of pass
    pass_circle = plt.Circle(xy=(x, pitchWidthY - y), radius=2, color='blue')
    # make the pass circles more transparent
    pass_circle.set_alpha(0.2)
    ax.add_patch(pass_circle)
    # set length of pass coordinates
    dx = the_pass['pass_end_location'][0] - x
    dy = the_pass['pass_end_location'][1] - y
    pass_arrow = plt.Arrow(x=x, y=pitchWidthY - y, dx=dx, dy=dy, width=2, color='blue')
    ax.add_patch(pass_arrow)

plt.title('Thierry Henry\'s pass map vs Manchester United on Sun 28 Mar 2004.')
plt.text(5, 75, 'Arsenal')
plt.text(110, 75, 'United')
fig.set_size_inches(10, 7)
# plt.savefig(Path('C:/Users/Philip/Desktop/python plots/Henry_passes_vs_united.pdf'))
plt.show()
