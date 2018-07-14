import pandas as pd
import json

df = pd.read_csv('json/Fixtures_matches.csv')

df = df[['awayTeam','homeTeam','matchday']]

# extract team names from strings (need to replace single quotes with double for json.loads)
df['awayTeam'] = [json.loads(x)['name'] for x in df['awayTeam'].str.replace("'",'"')]
df['homeTeam'] = [json.loads(x)['name'] for x in df['homeTeam'].str.replace("'",'"')]

# remove FC from team names
df['awayTeam'] = df['awayTeam'].str.replace(' FC','')
df['awayTeam'] = df['awayTeam'].str.replace(' AFC','')
df['awayTeam'] = df['awayTeam'].str.replace('AFC ','')
df['homeTeam'] = df['homeTeam'].str.replace(' FC','')
df['homeTeam'] = df['homeTeam'].str.replace(' AFC','')
df['homeTeam'] = df['homeTeam'].str.replace('AFC ','')

teams = df['homeTeam'].unique()

def opponent(row,team):
    if row.Stadium=='Home':
        return row.awayTeam
    else:
        return row.homeTeam

fixtures = {}
for team in teams:
    df_team = df[(df.awayTeam==team)|(df.homeTeam==team)]
    
    df_team['Stadium'] = df_team['homeTeam']==team
    df_team['Stadium'] = df_team['Stadium'].replace({True:'Home',False:'Away'}).astype('category')
    
    df_team['Opponent'] = df_team.apply(opponent,axis=1,args=(team,))
    
    df_team.set_index('matchday',inplace=True,drop=True)
    fixtures[team] = df_team[['Opponent','Stadium']]
    
print(fixtures['Chelsea'])