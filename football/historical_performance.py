from espn_api.football import League

# Init
league = League(league_id=235837, year=2019, username='mercinator486', password='Throwaway123$')
settings = league.settings

# Print teams to test
teams = league.teams
for team in teams:
    print("%s's team name is %s" % (team.owner, team.team_name))

# Leage average number of points per week, regular season
nweeks_regular = settings.reg_season_count


