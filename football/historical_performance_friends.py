from espn_api.football import League
import pickle
from pathlib import Path
import sys

# League info for the friends league
from leagueInfo_friends import *

# Years to run history for
years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

# Location to save pkl file or lookup saved data
fileDir = "."
fileName = "friends_league_history_data.pkl"
filePath = Path(fileDir + "/" + fileName)

# If the file already exists then load it instead of pulling from espn
if filePath.is_file():
    # file exists
    print("File exists, loading league data from " + fileName)
    Leagues = pickle.load( open(filePath, "rb" ) )
    # Check that the saved file matches the requested league id and years
    for n, league in enumerate(Leagues):
        if(league.league_id == id and league.year == years[n]):
            continue
        else:
            print("Error: loaded list does not match requested years or League id. Delete the pkl file in the directory and re-run")
            sys.exit()

else:
    # File does not exist
    print("No league data on disk, pulling requested years from ESPN...")
    # Pull all the leage data from espn
    Leagues = []
    for y in years:
        L = League(league_id=id, year=y, swid=swid, espn_s2=espn_s2)
        Leagues.append(L)
        print("Pulled league data for year = ", y)

    # Save the list of leagues to disk for future access
    open_file = open(filePath,'wb')
    pickle.dump(Leagues, open_file)
    open_file.close()

# Now loop on leagues and get a list of all the owners
owners = []
for league in Leagues:
    teams = league.teams
    for team in teams:
        if(team.owner not in owners):
            owners.append(team.owner)

# Printer a list of all owners over time
print("List of owners from " + str(years[0]) + " to " + str(years[-1]) )
print("------------------------------")
for owner in owners:
    print(owner)

# Now loop on owners and get historical data for them
seasonsPlayed = [0]*len(owners)
gamesPlayed = [0]*len(owners)
h2hwins = [0]*len(owners)
pointsFor = [0]*len(owners)
pointsAgainst = [0]*len(owners)
ppg = [0]*len(owners)
winsPerSeason = [0]*len(owners)
championships = [0]*len(owners)
for ownerIndex, owner in enumerate(owners):
    # Loop over each league year
    for n, league in enumerate(Leagues):
        # Find the owner for this league year
        for i, team in enumerate(league.teams):
            if(owner == team.owner):
                # print("Found owner %s for year %i" % (owner, years[n]))
                # Accumulate stats for the owner
                h2hwins[ownerIndex] += team.wins
                pointsFor[ownerIndex] += team.points_for
                pointsAgainst[ownerIndex] += team.points_against
                seasonsPlayed[ownerIndex] += 1
                gamesPlayed[ownerIndex] += len(team.schedule) # Number of games played this season
                if(team.final_standing==1):
                    championships[ownerIndex] += 1
                # Stop the search for owner in this league year
                break
            if(i==len(league.teams)-1):
                # print("Did not find owner %s for year %i" % (owner, years[n]))
                '''
                # Debug: confirm owner not found for given year
                if(i == len(league.teams)-1 ):
                    print(owner, " not found for year", league.year)
                '''

    # Season or per game averages
    ppg[ownerIndex] = pointsFor[ownerIndex]/gamesPlayed[ownerIndex]
    winsPerSeason[ownerIndex] = h2hwins[ownerIndex]/seasonsPlayed[ownerIndex]

# Print stats
print("="*145)
print("Historical Performance for years %i to %i" % (years[0], years[-1]) )
print("Season stats (all-time measures are regular season only)")
print("%20s %20s %20s %25s %25s %30s" % ("Owner", "Seasons Played", "Championships", "All Time H2H Wins", "All Time Points for", "All Time Points Against"))
#print("----------------------------------------------------")
print("="*145)
for i, owner in enumerate(owners):
    print("%20s %20i %20i %25i %25.2f %30.2f" % (owner, seasonsPlayed[i], championships[i], h2hwins[i], pointsFor[i], pointsAgainst[i]) )

# Print stat averages
print("="*120)
print("Historical Performance for years %i to %i" % (years[0], years[-1]) )
print("Regular season per-game and per-season metrics")
print("%20s %20s %20s %25s %20s" % ("Owner", "Seasons Played", "Games Played", "H2H Wins per season", "Points Per Game"))
#print("----------------------------------------------------")
print("="*120)
for i, owner in enumerate(owners):
    print("%20s %20i %20i %25.2f %20.2f" % (owner, seasonsPlayed[i], gamesPlayed[i], winsPerSeason[i], ppg[i]) )
