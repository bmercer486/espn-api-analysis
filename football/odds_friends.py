from espn_api.football import League
from standingsFunctions import *
from playoffOddsFunctions import *
import numpy as np
import pandas as pd
import time
import csv
import sys

# Leage data
id = 235837
year = 2021
swid='960A4466-0190-46A6-926B-4C7411602D3B'
espn_s2='AEC1%2BEdz7P6rOeLgGrgN163zuJFd65XBRcdxIoBDZ62cOYs0fTwu9XmlSl6tpkVyAMdB27LeKUJKiyMwpjfW%2B%2BxwCXMvN3qa8GWKDyMq0WxgC5EZy1TSU3Ws6DVbW2GSYr7kZwIKjL%2BKER4VhxC%2BUQ7RAH2SVtfSWn2RxibenHT%2FagC1ijS%2BAgz4YQ47QeS3adaNl7WB%2FFUh9nAliyVf8TYScLPkhiaxOUkAZ3tVjsxtAMFATxHv3Ylpjz%2BU5yuUBqn5jR2%2FDM%2FaPN%2BCe9Zb0FLu'
# For saving simulation results'
leaguename = 'friends'

# Define the league
league = League(league_id=id, year=year, swid=swid, espn_s2=espn_s2)

# What is the current week?
# league.current_week gives the current week real-time
week_current = league.current_week
week_current = 14

# Last week of the regular season
week_end = 14 # final week to consider for calculating odds

# Don't do calculation if it is requested for week at or beyond end of regular season
if(week_current > week_end):
    print("Error: Current week is at or beyond end of regular season")
    sys.exit()

# List of teams
teams = league.teams

# Teams, seeds, extra WL settings
nteams = len(teams)
nseeds = 6
extraWL = True

# Simulation settings
seed = 2021 # Arbitrary
rng = np.random.default_rng(seed)
# Distribution is 'normal', 'lognormal', or 'random'
distribution = 'random'
nsim = 100000

# The 'outcomes' array stores how many times each team got a particular seed
# The row is the team and the column is the outcome
# e.g. outcomes[3,1] will be how often team #3 in the 'teams' list
# got 2nd place in the final standings
outcomes = np.zeros( (nteams,nteams), dtype=int)
start_time = time.time()
for n in range(nsim):
    simulated_standings = simSeason(league, week_current, week_end, extraWL, rng, distribution)
    sim_record = simulated_standings[0]
    sim_total_wins = sim_record[::,0]
    sim_total_points_for = simulated_standings[1]

    # Once you have the standings, the playoff seeding needs to be determined by the league rules
    index = np.lexsort( (sim_total_points_for, sim_total_wins) )[::-1] # Numpy array of integers

    # Fill out the 'outcomes' array for this iteration
    for i in range(nteams):
        # 'i' represents finishing place from first to worst
        # first place team is index[0]
        # Second place team is index[1]
        # etc...
        outcomes[index[i]][i] += 1

# Simulation execution time
end_time = time.time()
runtime = end_time - start_time
print("Took ",runtime, " sec to simulate ",nsim, " seasons")

# Print current standings to check that predictions make sense
print("Current standings")
s = standings(league, week_current-1, extraWL)
printStandings(s, teams, week_current-1)

# Compute final probabilities as percentages
prob = (outcomes/nsim)*100

# Playoff odds Is the sum of odds to make any playoff seed
playoffOdds = []
seed1 = []
seed2 = []
seed3 = []
seed4 = []
seed5 = []
seed6 = []
for idx, t in enumerate(teams):
    playoffOdds.append(sum(prob[idx][0:nseeds]))
    seed1.append(prob[idx][0])
    seed2.append(prob[idx][1])
    seed3.append(prob[idx][2])
    seed4.append(prob[idx][3])
    seed5.append(prob[idx][4])
    seed6.append(prob[idx][5])

# Save into pandas dataframe for plotting later
df = pd.DataFrame({"Team name": [t.team_name for t in teams],
                   "Percent chance to make playoffs": playoffOdds,
                   "Percent chance to make 1 seed": seed1,
                   "Percent chance to make 2 seed": seed2,
                   "Percent chance to make 3 seed": seed3,
                   "Percent chance to make 4 seed": seed4,
                   "Percent chance to make 5 seed": seed5,
                   "Percent chance to make 6 seed": seed6,
                   })

# Print to check it
# print(df)

# Save it for later
filename = leaguename + "_playoff_odds" + "_heading_into_week" + str(week_current) + ".pkl"
df.to_pickle(filename)

# Write results to csv file
filename = "playoff_odds_" + leaguename + "_heading_into_week_" + str(week_current) + "_year_" + str(year) + ".csv"
with open(filename, mode='w', newline='') as csvfile:
    fwriter = csv.writer(csvfile)
    fwriter.writerow(['Team name','% chance make playoffs','% chance 1 seed','% chance 2 seed','% chance 3 seed','% chance 4 seed','% chance 5 seed','% chance 6 seed'])
    for idx, t in enumerate(teams):
        lst = [t.team_name, sum(prob[idx][0:nseeds]), prob[idx][0], prob[idx][1], prob[idx][2], prob[idx][3],prob[idx][4],prob[idx][5]]
        fwriter.writerow(lst)
