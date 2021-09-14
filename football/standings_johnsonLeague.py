from espn_api.football import League
from standingsFunctions import *
import numpy as np

# League info
id = 906364
year = 2021
swid = '960A4466-0190-46A6-926B-4C7411602D3B'
espn_s2 =  'AEBZY7c0EB8kSiEbA3guFdDr3H7bmSnSPEmxEXiaEeEz4kfMGA6%2BDxk3U3eznlcz9lquh0Tw86tX220Bcz%2FCBU8ynKt57Z6ERGrGwY8XpwvcSwIf2o8IfSEL7C%2BVH8FNKhKLDa34sSGsEUReuTSrTSrYWqax1l0hSgcDADebrE%2FWcSgAo6GMXOd%2Fp9vF8pYcehYt4fmlVJx4NBysKrboEPXdith2XzWvOVSWdyKe7PVWSp7TtFjkmritmcyacT4Tdxi8gt2Kn5QVbiQqE5wVoVJf'
# For saving simulation results
leaguename = 'Johnson\'s League'

# Get league
league = League(league_id=id, year=year, swid=swid, espn_s2=espn_s2)

# Get teams
teams = league.teams

# Week to get the standings through
week = league.current_week-1

# Do we use extra win-loss?
extraWL = True

# Old way
# print("League = ", leaguename)
# printStandings(league, week)
# print("")
# printWeeklyMostPoints(league, week)

# New way
print("League = ", leaguename)
s = standings(league, week, extraWL)
printStandings(s, teams, week)
print("")
printWeeklyMostPoints(s, week)
