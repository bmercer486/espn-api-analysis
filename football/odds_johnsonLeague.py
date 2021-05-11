from espn_api.football import League
from standingsFunctions import *
import numpy as np
import time
import csv

id = 906364
year = 2020
swid = '960A4466-0190-46A6-926B-4C7411602D3B'
espn_s2 =  'AEBZY7c0EB8kSiEbA3guFdDr3H7bmSnSPEmxEXiaEeEz4kfMGA6%2BDxk3U3eznlcz9lquh0Tw86tX220Bcz%2FCBU8ynKt57Z6ERGrGwY8XpwvcSwIf2o8IfSEL7C%2BVH8FNKhKLDa34sSGsEUReuTSrTSrYWqax1l0hSgcDADebrE%2FWcSgAo6GMXOd%2Fp9vF8pYcehYt4fmlVJx4NBysKrboEPXdith2XzWvOVSWdyKe7PVWSp7TtFjkmritmcyacT4Tdxi8gt2Kn5QVbiQqE5wVoVJf'
# For saving simulation results
leaguename = 'Johnson\'s League'

# Define the league
league = League(league_id=id, year=year, swid=swid, espn_s2=espn_s2)

# Team objects
teams = league.teams

# League info
# week_current = league.current_week # not yet played out
week_current = 10
week_end = 13 # final week to consider for calculating odds
nteams = len(teams)
nseeds = 6

# Get the league standings
s = standings(league,week_current,True)
record = s[0]
current_points_for = s[1]
current_wins = record[::,0]
print(s)

# Print the standings if desired
#print(leaguename)
#printStandings(league, week)

# List of the remaining weeks
weeks_remaining = list(range(week_current,week_end+1))

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

nsim = 1
start_time = time.time()
for n in range(nsim):
    # Loop on teams to simulate future scores for each team
    simulated_scores = [[0] * len(weeks_remaining) for i in range(nteams)]
    # simulated_scores = [ [0, 0, 0] ]*8 # Replace 3 zeros with general number of weeks remaining
    simulated_wins = [0] * nteams
    simulated_points_for = [0] * nteams
    total_wins = []
    total_points_for = []

    # Simulate scores in remaining weeks
    weekly_scores = []
    for idx_t, t in enumerate(teams):
        # Simulate one score for each remaining week
        # Score simulation based on team's avg score/week and stdev
        for idx_w, w in enumerate(weeks_remaining):
            # Later use e.g. normal distribution for this team's scoring history
            simulated_scores[idx_t][idx_w] = np.random.normal(avg[idx_t],stdev[idx_t])

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

    # Sort the standings in descending order and get the index to match up with teams
    # Sort on Total Wins and then Total Points For
    index = np.lexsort( (total_points_for, total_wins) )[::-1] # Numpy array of integers

    '''
    In Johnson's league, top 4 playoff teams are by record, then seeds 5 and 6 are by most points among the remaining 6 teams

    So what you want to do is get 2 groups: top4 (seeds 1-4) and wildcard (seeds 5 and 6)
    '''

    # The top 4 teams by record
    top4 = list(index[0:4])

    # For wildcard, sort by points only, but only take indices 4:end
    sorted_by_score_only = np.argsort(total_points_for)[::-1]
    wildcard = list() # Empty
    # Add teams to the wildcard list only if they aren't in the top 4
    for i in sorted_by_score_only:
        if i not in top4:
            wildcard.append(i)

    # Standings array is a list of the team indices from first to last
    standings = top4.copy()
    standings.extend(wildcard) # top4, followed by wildcard

    # # Debug
    # print(top4)
    # print(sorted_by_score_only)
    # print(wildcard)
    # print(standings[9])
    # print(len(top4))
    # print(len(wildcard))
    # print(standings)

    '''
    For your outcomes array, you want:
    outcomes[0:4] is correct according to index[i] as below
    outcomes[4::] should be based on sort_index_total_points but excluding the top 4 teams
    So it's probably smart to just make a list that includes those 6 teams ordered
    '''
    # Fill out the 'outcomes' array for this iteration
    for i in range(nteams):
        # 'i' represents finishing place from first to worst
        # first place team is index[0]
        # ---> Use "standings" rather than "index" to get the wildcard ranking right
        # etc...
        outcomes[standings[i]][i] += 1

    # Debugging: Print the standings
    print("Final Standings:")
    for i in standings:
        print(teams[i].team_name, total_wins[i], total_points_for[i])

    print("==============================")

# Compute final probabilities as percentages
prob = (outcomes/nsim)*100
# Write results to csv file
filename = "playoff_odds_" + leaguename + "_heading_into_week" + str(week_current) + ".csv"
with open(filename, mode='w', newline='') as csvfile:
    fwriter = csv.writer(csvfile)
    fwriter.writerow(['Team name','% chance make playoffs','% chance 1 seed','% chance 2 seed','% chance 3 seed','% chance 4 seed','% chance 5 seed','% chance 6 seed'])
    for idx, t in enumerate(teams):
        lst = [t.team_name, sum(prob[idx][0:nseeds]), prob[idx][0], prob[idx][1], prob[idx][2], prob[idx][3], prob[idx][4], prob[idx][5]]
        fwriter.writerow(lst)

# Simulation execution time
end_time = time.time()
runtime = end_time - start_time
print("Run time: ",runtime, " sec")
