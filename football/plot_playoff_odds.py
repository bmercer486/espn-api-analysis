from espn_api.football import League
import pickle
from pathlib import Path
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# # League info for the friends league
# ID = 235837
# year = 2021
# league_swid = '960A4466-0190-46A6-926B-4C7411602D3B'
# league_espn_s2 = 'AEC1%2BEdz7P6rOeLgGrgN163zuJFd65XBRcdxIoBDZ62cOYs0fTwu9XmlSl6tpkVyAMdB27LeKUJKiyMwpjfW%2B%2BxwCXMvN3qa8GWKDyMq0WxgC5EZy1TSU3Ws6DVbW2GSYr7kZwIKjL%2BKER4VhxC%2BUQ7RAH2SVtfSWn2RxibenHT%2FagC1ijS%2BAgz4YQ47QeS3adaNl7WB%2FFUh9nAliyVf8TYScLPkhiaxOUkAZ3tVjsxtAMFATxHv3Ylpjz%2BU5yuUBqn5jR2%2FDM%2FaPN%2BCe9Zb0FLu'

# Load the file if it exists
fileDir = "odds_2021_files"
fileName = "friends_playoff_odds_heading_into_week12.pkl"
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
p6 = ax.bar(ind, seed6, width, label='6 seed')
p5 = ax.bar(ind, seed5, width, label='5 seed', bottom=seed6)
p4 = ax.bar(ind, seed4, width, label='4 seed', bottom=seed5+seed6)
p3 = ax.bar(ind, seed3, width, label='3 seed', bottom=seed4+seed5+seed6)
p2 = ax.bar(ind, seed2, width, label='2 seed', bottom=seed3+seed4+seed5+seed6)
p1 = ax.bar(ind, seed1, width, color="tab:cyan", label='1 seed', bottom=seed2+seed3+seed4+seed5+seed6)

# Labels etc
ax.set_title('Playoff odds for each team: week xxx')
ax.set_ylabel('Probability')
ax.set_xticks(ind)
ax.set_xticklabels(teams, rotation=45, rotation_mode="anchor", ha="right")
ax.set_ylim([0, 110])
plt.gcf().subplots_adjust(bottom=0.4) # Fits long team names on x axis
ax.legend()

# Label the top of each bar with the chance of making the playoffs (sum of all seed probs)
ax.bar_label(p1)

plt.show()






# nteams = len(standings_df['Team name'])
# team_names = [None]*nteams
# for n in range(nteams):
#     team_names[n] = standings_df['Team name'][n]
#
# print(team_names)

# teams = [name for names in standings_df['Team name']]
# print(teams)
# # Get the playoff odds for each team
# # Playoff odds Is the sum of odds to make any playoff seed
# playoffOdds = []
# seed1 = []
# seed2 = []
# seed3 = []
# seed4 = []
# seed5 = []
# seed6 = []
# for idx, t in enumerate(teams):
#     playoffOdds.append(sum(prob[idx][0:nseeds]))
#     seed1.append(prob[idx][0])
#     seed2.append(prob[idx][1])
#     seed3.append(prob[idx][2])
#     seed4.append(prob[idx][3])
#     seed5.append(prob[idx][4])
#     seed6.append(prob[idx][5])

# else:
#     # File does not exist
#     print("No league data on disk, pulling requested years from ESPN...")
#     # Pull all the leage data from espn
#     Leagues = []
#     for y in years:
#         L = League(league_id=ID, year=y, swid=league_swid, espn_s2=league_espn_s2)
#         Leagues.append(L)
#         print("Pulled league data for year = ", y)
#
#     # Save the list of leagues to disk for future access
#     open_file = open(filePath,'wb')
#     pickle.dump(Leagues, open_file)
#     open_file.close()
#
# # Now loop on leagues and get a list of all the owners
# owners = []
# for league in Leagues:
#     teams = league.teams
#     for team in teams:
#         if(team.owner not in owners):
#             owners.append(team.owner)
#
# # Printer a list of all owners over time
# print("List of owners from " + str(years[0]) + " to " + str(years[-1]) )
# print("------------------------------")
# for owner in owners:
#     print(owner)
#
# # Now loop on owners and get historical data for them
# seasonsPlayed = [0]*len(owners)
# gamesPlayed = [0]*len(owners)
# h2hwins = [0]*len(owners)
# pointsFor = [0]*len(owners)
# pointsAgainst = [0]*len(owners)
# ppg = [0]*len(owners)
# winsPerSeason = [0]*len(owners)
# championships = [0]*len(owners)
# for ownerIndex, owner in enumerate(owners):
#     # Loop over each league year
#     for n, league in enumerate(Leagues):
#         # Find the owner for this league year
#         for i, team in enumerate(league.teams):
#             if(owner == team.owner):
#                 # print("Found owner %s for year %i" % (owner, years[n]))
#                 # Accumulate stats for the owner
#                 h2hwins[ownerIndex] += team.wins
#                 pointsFor[ownerIndex] += team.points_for
#                 pointsAgainst[ownerIndex] += team.points_against
#                 seasonsPlayed[ownerIndex] += 1
#                 gamesPlayed[ownerIndex] += len(team.schedule) # Number of games played this season
#                 if(team.final_standing==1):
#                     championships[ownerIndex] += 1
#                 # Stop the search for owner in this league year
#                 break
#             if(i==len(league.teams)-1):
#                 # print("Did not find owner %s for year %i" % (owner, years[n]))
#                 '''
#                 # Debug: confirm owner not found for given year
#                 if(i == len(league.teams)-1 ):
#                     print(owner, " not found for year", league.year)
#                 '''
#
#     # Season or per game averages
#     ppg[ownerIndex] = pointsFor[ownerIndex]/gamesPlayed[ownerIndex]
#     winsPerSeason[ownerIndex] = h2hwins[ownerIndex]/seasonsPlayed[ownerIndex]
#
# # Print stats
# print("="*145)
# print("Historical Performance for years %i to %i" % (years[0], years[-1]) )
# print("Season stats (all-time measures are regular season only)")
# print("%20s %20s %20s %25s %25s %30s" % ("Owner", "Seasons Played", "Championships", "All Time H2H Wins", "All Time Points for", "All Time Points Against"))
# #print("----------------------------------------------------")
# print("="*145)
# for i, owner in enumerate(owners):
#     print("%20s %20i %20i %25i %25.2f %30.2f" % (owner, seasonsPlayed[i], championships[i], h2hwins[i], pointsFor[i], pointsAgainst[i]) )
#
# # Print stat averages
# print("="*120)
# print("Historical Performance for years %i to %i" % (years[0], years[-1]) )
# print("Regular season per-game and per-season metrics")
# print("%20s %20s %20s %25s %20s" % ("Owner", "Seasons Played", "Games Played", "H2H Wins per season", "Points Per Game"))
# #print("----------------------------------------------------")
# print("="*120)
# for i, owner in enumerate(owners):
#     print("%20s %20i %20i %25.2f %20.2f" % (owner, seasonsPlayed[i], gamesPlayed[i], winsPerSeason[i], ppg[i]) )
