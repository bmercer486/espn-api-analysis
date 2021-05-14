from espn_api.football import League
from standingsFunctions import *
import numpy as np
import time
import csv
import sys

def simSeason(league, week_current, week_end, extraWL, rng, distribution='normal'):

    # Don't do calculation if it is requested for week at or beyond end of regular season
    if(week_current > week_end):
        print("Error: Current week is at or beyond end of regular season")
        sys.exit()

    # List of teams
    teams = league.teams

    # Number of teams
    nteams = len(teams)

    # Get the league standings
    current_standings = standings(league,week_current,extraWL)
    current_record = current_standings[0]
    current_points_for = current_standings[1]
    current_wins = current_record[::,0]

    # Print the standings if desired
    #print(leaguename)
    #printStandings(league, week)

    # List of completed weeks with score history
    weeks_completed = list(range(1,week_current))

    # List of the remaining weeks to be played
    weeks_remaining = list(range(week_current,week_end+1))

    # List of all weeks
    allweeks = list(range(1,week_end+1))

    # Compute each team's mean and stdev for scoring history
    avg = []
    stdev = []
    for t in teams:
        # Only go from 0 to (current week - 2)
        # If you wanted to include the current week you would have done
        # Up to current week - 1 but that hasn't been played yet
        avg.append(np.mean(t.scores[0:week_current-2]))
        stdev.append(np.std(t.scores[0:week_current-2]))

    # Compute average score per team based on total points in season
    league_avg = np.mean(avg)
    # League stdev = sum(variances)/N, take the sart
    league_stdev = np.sqrt(sum(np.square(stdev))/nteams)

    # Log normal parameters
    m = []
    s = []
    for idx_t, t in enumerate(teams):
        m.append(np.log( (avg[idx_t]**2)/np.sqrt(avg[idx_t]**2 + stdev[idx_t]**2) ))
        s.append(np.sqrt(np.log( 1 + avg[idx_t]**2/stdev[idx_t]**2)))

    # Actual and simulated scores for the whole season
    allscores = np.zeros((nteams,week_end))

    # Simulate scores in season
    for idx_t, t in enumerate(teams):
        for idx_w, w in enumerate(allweeks):
            # If week has been played, get it from team data
            if(w < week_current):
                allscores[idx_t][idx_w] = t.scores[idx_w]
            # If the week has not been played, then simulate it
            else:
                if(distribution == 'normal'):
                    # Normal distribution draw
                    allscores[idx_t][idx_w] = rng.normal(avg[idx_t], stdev[idx_t])
                if(distribution == 'lognormal'):
                    # Log normal distribution draw
                    allscores[idx_t][idx_w] = rng.lognormal(m[idx_t], s[idx_t])
                if(distribution == 'random'):
                    # All teams perform according to the same distribution, assumed normal
                    allscores[idx_t][idx_w] = rng.normal(league_avg, league_stdev)

    # Get the standings based on simulated season-end results
    simulated_standings = standingsGivenScores(allscores, teams, extraWL)

    # # Debugging: Print the standings
    # print("Final Standings:")
    # for i in index:
    #     print(teams[i].team_name, sim_total_wins[i], total_points_for[i])

    # # Debugging: check total wins
    # for i in index:
    #     print(teams[i].team_name, sim_total_wins[i], total_points_for[i])

    return simulated_standings
