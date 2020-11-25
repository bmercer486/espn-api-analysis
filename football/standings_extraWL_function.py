from espn_api.football import League
import numpy as np
import csv

def standings(league, week, extraWL=False):

    """
    league: espn-api League object
    week: integer, the week you want standings through. e.g. week = 4 gives the standings after 4 weeks of
    play
    extraWL: boolean, False just gets h2h wins, True adds on extra W/L for top/bottom half of teams

    Returns a tuple with four entries:
    [0] = Ranked list of teams (first in list is in first place)
    [1] = numpy array, rows are each team, columns are win/loss/tie counts
    [2] = List of total points scored for each team
    [3] = List of weekly most points winners
    """

    # Import the league teams
    teams = league.teams

    # Number of teams in the league
    nteams = len(teams)

    """
    Use this block to get H2H wins from espn data
    Only works if you want the current standings at present
    current_points_for = []
    current_wins = []
    # # Head to head wins - get using current week
    # for t in teams:
    #     current_wins.append(t.wins)
    #     current_points_for.append(t.points_for)
    """

    # Head to head wins - determine by matchup, per week, manually
    points_for = [0] * nteams
    wins = [0] * nteams
    # record[i,0] = total wins for team i
    # record[i,1] = total losses for team i
    # record[i,2] = total ties for team i
    record = np.zeros( (nteams,3), dtype=int)
    for idx_t, t in enumerate(teams):
        for w in range(0,week):
            # Accumulate points for
            points_for[idx_t] += t.scores[w]
            # Find this week's opponent for team 't'
            opponent = t.schedule[w] # Team object: opponent in week 'w'
            opponent_idx = teams.index(opponent)
            # Accumulate H2H win if earned
            if(t.scores[w] > opponent.scores[w]):
                wins[idx_t] += 1
                record[idx_t,0] += 1
            elif(t.scores[w] < opponent.scores[w]):
                record[idx_t,1] += 1
            elif(t.scores[w] == opponent.scores[w]):
                record[idx_t,2] += 1

    """
    # These 3 variables will have the same index and match on those indexes
    schedule: List[Team]
    scores: List[int]
    outcomes: List[str]
    """

    # Standings including the extra W/L for top half/bottom half teams on a weekly basis
    if(extraWL):
        weekly_points_winners = []
        for w in range(0,week):
            weekly_scores = []
            # Get scores for each team
            for idx_t, t in enumerate(teams):
                weekly_scores.append(t.scores[w])
            # Sort the scores for the week
            sorted_teams = np.argsort(weekly_scores)[::-1]
            # cutoff_score: score of team #5 - any below this is bottom 5
            cutoff_position = int(nteams/2) # List index of cutoff team
            cutoff_idx = sorted_teams[cutoff_position-1] # 5th ranking team this week
            cutoff_score = weekly_scores[cutoff_idx]
            # Check for ties
            tied_idx = []
            extraWL_tie = False
            for idx_t, t in enumerate(teams):
                # Don't check equality on the team with cutoff score
                if(idx_t != cutoff_idx):
                    # If this team's score is equal to the 5th ranked team's score, then these teams are involved in a tie
                    if(weekly_scores[idx_t] == cutoff_score):
                        tied_idx.append(idx_t)
            # If tied_idx has nonzero length, then be sure to add team #5 into the list as a team who has a tie
            if(len(tied_idx) > 0):
                tied_idx.append(cutoff_idx)
            # Assign wins to top half of teams - [0:n] does *not* include end item
            for i in sorted_teams[0:cutoff_position]:
                # If the team is involved in a tie, record a tie and not a win
                if(i in tied_idx):
                    record[i,2] +=1
                # Record a win
                else:
                    wins[i] += 1
                    record[i,0] += 1
            # Assign losses to bottom half of teams - [n::] includes item n til the end of list
            for i in sorted_teams[cutoff_position::]:
                # If the team is involved in a tie, record a tie and not a loss
                if(i in tied_idx):
                    record[i,2] += 1
                # Record a loss
                else:
                    record[i,1] += 1

            # Identify the winner of most weekly points
            weekly_points_winners.append(teams[sorted_teams[0]])
            # Also the above assumes 10 teams

    # Return the record, points for, and weekly points weekly_points_winners
    return record, points_for, weekly_points_winners

"""
    # Sort the standings in descending order and get the index to match up with teams
    # Sort on Total Wins and then Total Points For
    index = np.lexsort( (points_for, wins) )[::-1] # Numpy array of integers

    # Return the sorted list of teams, their record, and points for
    current_standings_teams = []
    sorted_record = np.zeros( (nteams,3), dtype=int )
    for i, irank in enumerate(index):
        current_standings_teams.append(teams[irank])
        sorted_record[i,::] = record[irank,::]

    return current_standings_teams, sorted_record, points_for, weekly_points_winners
"""

def printStandings(league, week):

    """
    s = standings(league, week, True)
    teams_ordered = s[0]
    record = s[1]
    points_for = s[2]
    """

    teams = league.teams
    nteams = len(teams)

    s = standings(league, week, True)
    record = s[0]
    points_for = s[1]

    # Sort the standings in descending order and get the index to match up with teams
    # Sort on Total Wins and then Total Points For
    index = np.lexsort( (points_for, record[::,0]) )[::-1] # Numpy array of integers

    # Return the sorted list of teams, their record, and points for
    ranked_teams = []
    sorted_record = np.zeros( record.shape, dtype=int )
    for i, irank in enumerate(index):
        ranked_teams.append(teams[irank])
        sorted_record[i,::] = record[irank,::]

    print("="*80)
    print("Standings Through Week %i" % (week) )
    print("%50s %12s %14s" % ("Team (Owner)", "Record", "Points for"))
    #print("----------------------------------------------------")
    print("="*80)
    for i, t in enumerate(ranked_teams):
        team_name_owner = t.team_name + " (" + t.owner + ")"
        rec = str(sorted_record[i,0])+"-"+str(sorted_record[i,1])+"-"+str(sorted_record[i,2])
        print("%50s %12s %14.2f" % (team_name_owner, rec, points_for[i]) )

def printWeeklyMostPoints(league, week):

    s = standings(league, week, True)
    weekly_points_winners = s[2]

    # Print weekly most points winners of weekly most points
    print("====================================================")
    print("Weekly most points")
    print("====================================================")
    for w in range(0, week):
        team_name_owner = weekly_points_winners[w].team_name + " (" + weekly_points_winners[w].owner + ")"
        print("Week %2i: %s" % (w+1, team_name_owner) )


# Test the functions
id = 906364
year = 2020
swid = '960A4466-0190-46A6-926B-4C7411602D3B'
espn_s2 =  'AEBZY7c0EB8kSiEbA3guFdDr3H7bmSnSPEmxEXiaEeEz4kfMGA6%2BDxk3U3eznlcz9lquh0Tw86tX220Bcz%2FCBU8ynKt57Z6ERGrGwY8XpwvcSwIf2o8IfSEL7C%2BVH8FNKhKLDa34sSGsEUReuTSrTSrYWqax1l0hSgcDADebrE%2FWcSgAo6GMXOd%2Fp9vF8pYcehYt4fmlVJx4NBysKrboEPXdith2XzWvOVSWdyKe7PVWSp7TtFjkmritmcyacT4Tdxi8gt2Kn5QVbiQqE5wVoVJf'
# For saving simulation results
leaguename = 'Johnson\'s League'

league = League(league_id=id, year=year, swid=swid, espn_s2=espn_s2)

# Week to get the standings through
week = league.current_week-1

print(leaguename)
printStandings(league, week)
print("")
printWeeklyMostPoints(league, week)
