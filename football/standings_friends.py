from espn_api.football import League
from standingsFunctions import *
import numpy as np

# League info
id = 235837
year = 2020
swid='960A4466-0190-46A6-926B-4C7411602D3B'
espn_s2='AEC1%2BEdz7P6rOeLgGrgN163zuJFd65XBRcdxIoBDZ62cOYs0fTwu9XmlSl6tpkVyAMdB27LeKUJKiyMwpjfW%2B%2BxwCXMvN3qa8GWKDyMq0WxgC5EZy1TSU3Ws6DVbW2GSYr7kZwIKjL%2BKER4VhxC%2BUQ7RAH2SVtfSWn2RxibenHT%2FagC1ijS%2BAgz4YQ47QeS3adaNl7WB%2FFUh9nAliyVf8TYScLPkhiaxOUkAZ3tVjsxtAMFATxHv3Ylpjz%2BU5yuUBqn5jR2%2FDM%2FaPN%2BCe9Zb0FLu'
# For saving simulation results'
leaguename = 'friends'

league = League(league_id=id, year=year, swid=swid, espn_s2=espn_s2)

# Week to get the standings through
week = league.current_week-1

print(leaguename)
printStandings(league, week)
print("")
printWeeklyMostPoints(league, week)
