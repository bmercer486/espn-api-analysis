from espn_api.football import League
from standingsFunctions import *
from playoffOddsFunctions import *
import numpy as np
import time
import csv
import sys

# Leage data
id = 235837
year = 2020
swid='960A4466-0190-46A6-926B-4C7411602D3B'
espn_s2='AEC1%2BEdz7P6rOeLgGrgN163zuJFd65XBRcdxIoBDZ62cOYs0fTwu9XmlSl6tpkVyAMdB27LeKUJKiyMwpjfW%2B%2BxwCXMvN3qa8GWKDyMq0WxgC5EZy1TSU3Ws6DVbW2GSYr7kZwIKjL%2BKER4VhxC%2BUQ7RAH2SVtfSWn2RxibenHT%2FagC1ijS%2BAgz4YQ47QeS3adaNl7WB%2FFUh9nAliyVf8TYScLPkhiaxOUkAZ3tVjsxtAMFATxHv3Ylpjz%2BU5yuUBqn5jR2%2FDM%2FaPN%2BCe9Zb0FLu'
# For saving simulation results'
leaguename = 'friends'

# Define the league
league = League(league_id=id, year=year, swid=swid, espn_s2=espn_s2)

# What is the current week?
# league.current gives the current week real-time
week_current = 4

# Last week of the regular season
week_end = 12 # final week to consider for calculating odds

# Don't do calculation if it is requested for week at or beyond end of regular season
if(week_current > week_end):
    print("Error: Current week is at or beyond end of regular season")
    sys.exit()

# List of teams
teams = league.teams

# Teams, seeds, extra WL settings
nteams = len(teams)
nseeds = 4
extraWL = True

# Simulation settings
seed = 2021 # Arbitrary
rng = np.random.default_rng(seed)
distribution = 'random'
nsim = 10000

# Get the simulated outcomes
outcomes = playoffOdds(league, nseeds, week_current, week_end, extraWL, rng, distribution, nsim)

# Print current standings to check that predictions make sense
print("Current standings")
s = standings(league, week_current, extraWL)
printStandings(s, teams, week_current)

# Compute final probabilities as percentages
prob = (outcomes/nsim)*100
# Write results to csv file
filename = "playoff_odds_" + leaguename + "_heading_into_week" + str(week_current) + ".csv"
with open(filename, mode='w', newline='') as csvfile:
    fwriter = csv.writer(csvfile)
    fwriter.writerow(['Team name','% chance make playoffs','% chance 1 seed','% chance 2 seed','% chance 3 seed','% chance 4 seed'])
    for idx, t in enumerate(teams):
        lst = [t.team_name, sum(prob[idx][0:nseeds]), prob[idx][0], prob[idx][1], prob[idx][2], prob[idx][3]]
        fwriter.writerow(lst)

# # Simulation execution time
# end_time = time.time()
# runtime = end_time - start_time
# print("Run time: ",runtime, " sec")
