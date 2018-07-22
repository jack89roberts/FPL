import pandas as pd
import json

# load fixtures file
df = pd.read_csv('json/Fixtures_matches.csv')

df = df[['awayTeam','homeTeam','matchday']]

# extract team names from strings (need to replace single quotes with double for json.loads)
df['awayTeam'] = [json.loads(x)['name'] for x in df['awayTeam'].str.replace("'",'"')]
df['homeTeam'] = [json.loads(x)['name'] for x in df['homeTeam'].str.replace("'",'"')]

# change team names to FPL equivalents
df.replace({'Manchester United FC':'Man Utd',
            'Newcastle United FC':'Newcastle',
            'Fulham FC':'Fulham',
            'Huddersfield Town AFC':'Huddersfield',
            'Watford FC':'Watford',
            'AFC Bournemouth':'Bournemouth',
            'Wolverhampton Wanderers FC':'Wolves',
            'Liverpool FC':'Liverpool',
            'Southampton FC':'Southampton',
            'Arsenal FC':'Arsenal',
            'Cardiff City FC':'Cardiff',
            'Tottenham Hotspur FC':'Spurs',
            'Everton FC':'Everton',
            'Leicester City FC':'Leicester',
            'Burnley FC':'Burnley',
            'West Ham United FC':'West Ham',
            'Chelsea FC':'Chelsea',
            'Manchester City FC':'Man City',
            'Brighton & Hove Albion FC':'Brighton',
            'Crystal Palace FC':'Crystal Palace'},
            inplace=True)

teams = df['homeTeam'].unique()

def opponent(row,team):
    #if row.Stadium=='Home':
    #    return row.awayTeam
    #else:
    #    return row.homeTeam
    if row.homeTeam==team:
        return (row.awayTeam,'Home')
    else:
        return (row.homeTeam,'Away')

fixtures = {}
for team in teams:
    df_team = df[(df.awayTeam==team)|(df.homeTeam==team)]
    
    #df_team['Stadium'] = df_team['homeTeam']==team
    #df_team['Stadium'] = df_team['Stadium'].replace({True:'Home',False:'Away'}).astype('category')
    
    df_team['Opponent'] = df_team.apply(opponent,axis=1,args=(team,))
    
    df_team.set_index('matchday',inplace=True,drop=True)
    #fixtures[team] = df_team[['Opponent','Stadium']]
    fixtures[team] = df_team['Opponent']

fixtures = pd.DataFrame(fixtures)

fixtures.to_csv('processed/fixtures.csv')