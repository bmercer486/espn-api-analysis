from espn_api.football import League
from standingsFunctions import *
import numpy as np
import time
import csv
import sys

id = 235837
year = 2020
swid='960A4466-0190-46A6-926B-4C7411602D3B'
espn_s2='AEC1%2BEdz7P6rOeLgGrgN163zuJFd65XBRcdxIoBDZ62cOYs0fTwu9XmlSl6tpkVyAMdB27LeKUJKiyMwpjfW%2B%2BxwCXMvN3qa8GWKDyMq0WxgC5EZy1TSU3Ws6DVbW2GSYr7kZwIKjL%2BKER4VhxC%2BUQ7RAH2SVtfSWn2RxibenHT%2FagC1ijS%2BAgz4YQ47QeS3adaNl7WB%2FFUh9nAliyVf8TYScLPkhiaxOUkAZ3tVjsxtAMFATxHv3Ylpjz%2BU5yuUBqn5jR2%2FDM%2FaPN%2BCe9Zb0FLu'
# For saving simulation results'
leaguename = 'friends'

# Define the league
league = League(league_id=id, year=year, swid=swid, espn_s2=espn_s2)

# League info
# week_current = league.current_week # not yet played out
week_current = 12
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

# Get the league standings
current_standings = standings(league,week_current,extraWL)
record = current_standings[0]
current_points_for = current_standings[1]
current_wins = record[::,0]

# Print the standings if desired
#print(leaguename)
#printStandings(league, week)

# List of the remaining weeks
weeks_remaining = list(range(week_current,week_end+1))

# List of all weeks
allweeks = list(range(1,week_end+1))

"""
# Get current standings and points
current_wins = [14, 13, 6, 13, 17, 9, 19, 4, 8, 7] # Enter manually for friends league
current_wins
current_points_for = []
for t in teams:
    # current_wins.append(t.wins)
    current_points_for.append(t.points_for)
"""

# Compute each team's mean and stdev for scoring history
avg = []
stdev = []
for t in teams:
    # Only go from 0 to (current week - 2)
    # If you wanted to include the current week you would have done
    # Up to current week - 1 but that hasn't been played yet
    avg.append(np.mean(t.scores[0:week_current-2]))
    stdev.append(np.std(t.scores[0:week_current-2]))

# The 'outcomes' array stores how many times each team got a particular seed
# The row is the team and the column is the outcome
# e.g. outcomes[3,1] will be how often team #3 in the 'teams' list
# got 2nd place in the final standings
outcomes = np.zeros( (nteams,nteams), dtype=int)

nsim = 10000
start_time = time.time()
for n in range(nsim):
    """
    # Loop on teams to simulate future scores for each team
    simulated_scores = [[0] * len(weeks_remaining) for i in range(nteams)]
    # simulated_scores = [ [0, 0, 0] ]*8 # Replace 3 zeros with general number of weeks remaining
    simulated_wins = [0] * nteams
    simulated_points_for = [0] * nteams
    """
    # total_wins = []
    # total_points_for = []
    allscores = np.zeros((nteams,week_end))

    # Simulate scores in season
    for idx_t, t in enumerate(teams):
        for idx_w, w in enumerate(allweeks):
            # If week has been played, get it from team data
            if(w < week_current):
                allscores[idx_t][idx_w] = t.scores[idx_w]
            # If the week has not been played, then simulate it
            else:
                # Normal distribution draw
                allscores[idx_t][idx_w] = np.random.normal(avg[idx_t],stdev[idx_t])

    # Get the standings based on simulated season-end results
    simulated_standings = standingsGivenScores(allscores, teams, extraWL)
    sim_record = simulated_standings[0]
    total_wins = sim_record[::,0]
    total_points_for = simulated_standings[1]

    """
    #Let the standings function figure out this part instead
    ================================================================
    # Loop on teams and figure out how many wins they have based on scores/schedule
    for idx_t, t in enumerate(teams):
        for idx_w, w in enumerate(weeks_remaining):
            # Find this week's opponent for team 't'
            opponent = t.schedule[w-1] # Team object: opponent in week 'w'
            opponent_idx = teams.index(opponent)
            # Accumulate H2H win if earned
            if(simulated_scores[idx_t][idx_w] > simulated_scores[opponent_idx][idx_w]):
                simulated_wins[idx_t] += 1
            # Accumulate top 5 win if earned
            week_scores = [item[idx_w] for item in simulated_scores]
            sorted_scores = np.argsort(week_scores)[::-1]
            # Top 5 cutoff is above sorted score with index 5 (5,6,7,8,9 are bottom 5)
            cutoff_score = week_scores[sorted_scores[5]]
            if(week_scores[idx_t] > cutoff_score):
                simulated_wins[idx_t] += 1


        # Compute final total wins and points for
        total_wins.append(current_wins[idx_t] + simulated_wins[idx_t])
        total_points_for.append(current_points_for[idx_t] + sum(simulated_scores[idx_t]) )
        """

    # Sort the standings in descending order and get the index to match up with teams
    # Sort on Total Wins and then Total Points For
    index = np.lexsort( (total_points_for, total_wins) )[::-1] # Numpy array of integers

    # Fill out the 'outcomes' array for this iteration
    for i in range(nteams):
        # 'i' represents finishing place from first to worst
        # first place team is index[0]
        # Second place team is index[1]
        # etc...
        outcomes[index[i]][i] += 1

    # # Debugging: Print the standings
    # print("Final Standings:")
    # for i in index:
    #     print(teams[i].team_name, total_wins[i], total_points_for[i])

# # Debugging: check total wins
# for i in index:
#     print(teams[i].team_name, total_wins[i], total_points_for[i])

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

# Simulation execution time
end_time = time.time()
runtime = end_time - start_time
print("Run time: ",runtime, " sec")
