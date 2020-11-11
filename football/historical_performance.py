from espn_api.football import League

# Init
#league = League(league_id=235837, year=2019, username='mercinator486', password='Throwaway123$')
league = League(league_id=235837, year=2019, swid='960A4466-0190-46A6-926B-4C7411602D3B',
espn_s2='AEC1%2BEdz7P6rOeLgGrgN163zuJFd65XBRcdxIoBDZ62cOYs0fTwu9XmlSl6tpkVyAMdB27LeKUJKiyMwpjfW%2B%2BxwCXMvN3qa8GWKDyMq0WxgC5EZy1TSU3Ws6DVbW2GSYr7kZwIKjL%2BKER4VhxC%2BUQ7RAH2SVtfSWn2RxibenHT%2FagC1ijS%2BAgz4YQ47QeS3adaNl7WB%2FFUh9nAliyVf8TYScLPkhiaxOUkAZ3tVjsxtAMFATxHv3Ylpjz%2BU5yuUBqn5jR2%2FDM%2FaPN%2BCe9Zb0FLu')
settings = league.settings

# Print teams to test
teams = league.teams
for team in teams:
    print("%s's team name is %s" % (team.owner, team.team_name))

# Leage average number of points per week, regular season
nweeks_regular = settings.reg_season_count


