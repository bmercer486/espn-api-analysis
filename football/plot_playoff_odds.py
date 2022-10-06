from espn_api.football import League
import pickle
from pathlib import Path
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Save the figure if true
save = True

# Manually set the week for the odds calculation
week = 5

# Load the file if it exists
fileDir = "."
fileName = "friends_playoff_odds_heading_into_week5_year2022_nsim100000.pkl"
filePath = Path(fileDir + "/" + fileName)
if filePath.is_file():
    # file exists
    print("File exists, loading league data from " + fileName)
    df = pickle.load( open(filePath, "rb" ) )
else:
    print("Error: pkl file does not exist")
    sys.exit()

# Print column headers
print(df.columns)

# Extract data for easier processing
teams = list(df['Team name'])
make_playoffs = np.array(df['Percent chance to make playoffs'])
seed1 = np.array(df['Percent chance to make 1 seed'])
seed2 = np.array(df['Percent chance to make 2 seed'])
seed3 = np.array(df['Percent chance to make 3 seed'])
seed4 = np.array(df['Percent chance to make 4 seed'])
seed5 = np.array(df['Percent chance to make 5 seed'])
seed6 = np.array(df['Percent chance to make 6 seed'])

# Plotting
N = len(teams)
width = 0.5        # the width of the bars: can also be len(x) sequence
ind = np.arange(N) # The x locations for the groups

# Stacked bar plot
fig, ax = plt.subplots()
p1 = ax.bar(ind, seed1, width, color="tab:cyan", label='1 seed', bottom=seed2+seed3+seed4+seed5+seed6)
p2 = ax.bar(ind, seed2, width, label='2 seed', bottom=seed3+seed4+seed5+seed6)
p3 = ax.bar(ind, seed3, width, label='3 seed', bottom=seed4+seed5+seed6)
p4 = ax.bar(ind, seed4, width, label='4 seed', bottom=seed5+seed6)
p5 = ax.bar(ind, seed5, width, label='5 seed', bottom=seed6)
p6 = ax.bar(ind, seed6, width, label='6 seed')

# Labels etc
ax.set_title('Playoff odds heading into week ' + str(week))
ax.set_ylabel('Probability')
ax.set_xticks(ind)
ax.set_xticklabels(teams, rotation=45, rotation_mode="anchor", ha="right")
ax.set_ylim([0, 110])
plt.gcf().subplots_adjust(bottom=0.4) # Fits long team names on x axis
ax.legend()
# Label the top of each bar with the chance of making the playoffs (sum of all seed probs)
ax.bar_label(p1)

# # Save the plot
# if(save==True):
#     # Strip off the .pkl and add .png
#     savename = fileName[:-4] + ".png"
#     print(savename)
#     plt.savefig(savename)

# Display
plt.show()
