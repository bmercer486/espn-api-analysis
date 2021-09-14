from espn_api.football import League
import pickle
import pandas as pd
from pathlib import Path
import sys
import matplotlib.pyplot as plt

# League info for the friends league
id = 235837
year = 2020
league_swid = '960A4466-0190-46A6-926B-4C7411602D3B'
league_espn_s2 = 'AEC1%2BEdz7P6rOeLgGrgN163zuJFd65XBRcdxIoBDZ62cOYs0fTwu9XmlSl6tpkVyAMdB27LeKUJKiyMwpjfW%2B%2BxwCXMvN3qa8GWKDyMq0WxgC5EZy1TSU3Ws6DVbW2GSYr7kZwIKjL%2BKER4VhxC%2BUQ7RAH2SVtfSWn2RxibenHT%2FagC1ijS%2BAgz4YQ47QeS3adaNl7WB%2FFUh9nAliyVf8TYScLPkhiaxOUkAZ3tVjsxtAMFATxHv3Ylpjz%2BU5yuUBqn5jR2%2FDM%2FaPN%2BCe9Zb0FLu'

# league = League(league_id=id, year=year, swid=league_swid, espn_s2=league_espn_s2)

# If the file already exists then load it instead of pulling from espn
oddsDataFiles = [
"friends_playoff_odds_heading_into_week6.pkl",
"friends_playoff_odds_heading_into_week7.pkl",
"friends_playoff_odds_heading_into_week8.pkl",
"friends_playoff_odds_heading_into_week9.pkl",
"friends_playoff_odds_heading_into_week10.pkl",
"friends_playoff_odds_heading_into_week11.pkl",
"friends_playoff_odds_heading_into_week12.pkl"
]
weeks = [6,7,8,9,10,11,12]

# Get team names from one dataframe
tempdf = pd.read_pickle(oddsDataFiles[0])
oddsDF = pd.DataFrame()
oddsDF.insert(0,'Team Name',tempdf['Team name'])

# Loop on data files to fill out the data frame, adding 1 column (week) at a time
for i, file in enumerate(oddsDataFiles):
    df = pd.read_pickle(file)
    # colName = 'Percent chance to make playoffs week ' + str(weeks[i])
    colName = 'Week ' + str(weeks[i])
    # Since i starts at 0, insert at column i + 1
    oddsDF.insert(i+1,colName,df['Percent chance to make playoffs'])

# Check the dataframe
print(oddsDF)

# Quick and dirty: plot each dataframe row.
# Each row is a team's playoff odds over the given weeks
nteams = 10
plt.figure()
for i in range(0,nteams):
    plt.plot(oddsDF.iloc[i,1::])

# Legend is created from converting the 'Team Name' DF column into a list
plt.legend(list(oddsDF.loc[:,'Team Name']))
plt.ylabel('% Chance of making playoffs, any seed')
plt.grid()
plt.show()
