HOME_ADVANTAGE = 1.1

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
    
####################################
# load fpl team info file
'''
difficulties = pd.read_csv('json/FPL_teams.csv')

difficulties = difficulties[['name',
                             'strength_attack_away',
                             'strength_attack_home',
                             'strength_defence_away',
                             'strength_defence_home',
                             'strength_overall_away',
                             'strength_overall_home',
                             'strength']]

difficulties.rename(columns={'name':'Opponent',
                             'strength_attack_away':'att_away',
                             'strength_attack_home':'att_home',
                             'strength_defence_away':'def_away',
                             'strength_defence_home':'def_home',
                             'strength_overall_away':'ovr_home',
                             'strength_overall_home':'ovr_away'},
                    inplace=True)

difficulties.set_index('Opponent',inplace=True)

difficulties = (difficulties/difficulties.max())**2

difficulties[['att_home','def_home','ovr_home']] = difficulties[['att_home','def_home','ovr_home']]*HOME_ADVANTAGE

print(difficulties)

def difficulty(row):
    if row['Stadium']=='Home':
        attack = difficulties.loc[row.Opponent,'def_away']
        defence = difficulties.loc[row.Opponent, 'att_away']
        overall = difficulties.loc[row.Opponent, 'ovr_away']
    else:
        attack = difficulties.loc[row.Opponent,'def_home']
        defence = difficulties.loc[row.Opponent, 'att_home']
        overall = difficulties.loc[row.Opponent, 'ovr_home']
        
    return pd.Series({'Opponent':row.Opponent,'Stadium':row.Stadium,
                      'Diff_Attack':attack,'Diff_Defence':defence,'Diff_Overall':overall})

for team in teams:
    fixtures[team] = fixtures[team].apply(difficulty,axis=1)

print(fixtures['Chelsea'])

import matplotlib.pyplot as plt
fixtures['Chelsea'].Diff_Attack.plot()
fixtures['Chelsea'].Diff_Defence.plot()
fixtures['Chelsea'].Diff_Overall.plot()
plt.show()
'''