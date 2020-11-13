from espn_api.football import League
import numpy as np
import csv

id = 235837
year = 2020
# For saving simulation results'
leaguename = 'friends'

league = League(league_id=235837, year=2020, swid='960A4466-0190-46A6-926B-4C7411602D3B',
espn_s2='AEC1%2BEdz7P6rOeLgGrgN163zuJFd65XBRcdxIoBDZ62cOYs0fTwu9XmlSl6tpkVyAMdB27LeKUJKiyMwpjfW%2B%2BxwCXMvN3qa8GWKDyMq0WxgC5EZy1TSU3Ws6DVbW2GSYr7kZwIKjL%2BKER4VhxC%2BUQ7RAH2SVtfSWn2RxibenHT%2FagC1ijS%2BAgz4YQ47QeS3adaNl7WB%2FFUh9nAliyVf8TYScLPkhiaxOUkAZ3tVjsxtAMFATxHv3Ylpjz%2BU5yuUBqn5jR2%2FDM%2FaPN%2BCe9Zb0FLu')

teams = league.teams

# League info
week_current = league.current_week # not yet played out
week_current = 5
nteams = len(teams)

# Get current standings and points
# Team order:
# Jordan
# Isaac
# Milburn
# Me
# Johnson
# Ewing
# Marieke
# Swanson
# Webbos
# Claude
current_points_for = []
current_wins = []
# # Head to head wins - get using current week
# for t in teams:
#     current_wins.append(t.wins)
#     current_points_for.append(t.points_for)

current_points_for = [0] * nteams
current_wins = [0] * nteams
# Head to head wins - determine by matchup, per week, manually
for idx_t, t in enumerate(teams):
    for w in range(0,week_current-1):
        # Accumulate points for
        current_points_for[idx_t] += t.scores[w]
        # Find this week's opponent for team 't'
        opponent = t.schedule[w-1] # Team object: opponent in week 'w'
        opponent_idx = teams.index(opponent)
        # Accumulate H2H win if earned
        if(t.scores[w] > opponent.scores[w]):
            current_wins[idx_t] += 1

"""
# These 3 variables will have the same index and match on those indexes
schedule: List[Team]
scores: List[int]
outcomes: List[str]

Algorithm for getting top 5 win
1. For each week w = 1, current_week:
  2. For each team:
     get the score for each team using team.scores[week]
     Store in array that follows team order
  3. Sort the scores using np.argsort
  4. Define the cutoff score
  5. For each team above the cutoff score, add a win
  ---> Check for ties?
"""

for w in range(0,week_current-1):
    weekly_scores = []
    for idx_t, t in enumerate(teams):
        weekly_scores.append(t.scores[w])
    # Sort the scores for the week
    sorted_scores = np.argsort(weekly_scores)[::-1]
    # Top 5 cutoff is above sorted score with index 5 (5,6,7,8,9 are bottom 5)
    cutoff_score = weekly_scores[sorted_scores[5]]
    for idx_t, t in enumerate(teams):
        if(weekly_scores[idx_t] > cutoff_score):
            current_wins[idx_t] += 1

# Sort the standings in descending order and get the index to match up with teams
# Sort on Total Wins and then Total Points For
index = np.lexsort( (current_points_for, current_wins) )[::-1] # Numpy array of integers

# Debugging: Print the standings
# print("Final Standings:")
print("Standings after week %2i" % (week_current-1) )
print("%30s %6s %12s" % ("Team name", "Wins", "Points for"))
print("----------------------------------------------------")
for i in index:
    print("%30s %6i %12.2f" % (teams[i].team_name, current_wins[i], current_points_for[i]) )
    #print(teams[i].team_name, current_wins[i], current_points_for[i])



"""
Algorithm for simulating scores - borrow some code here

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

"""
