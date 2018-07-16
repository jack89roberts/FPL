import pandas as pd
import ast

results = pd.read_csv('json/Results_matches.csv')

# only completed matches
results = results[results.status=='FINISHED']

# extract team names from strings (need to replace single quotes with double for json.loads)
results['awayTeam'] = [x['name'] for x in results['awayTeam'].apply(ast.literal_eval)]
results['homeTeam'] = [x['name'] for x in results['homeTeam'].apply(ast.literal_eval)]

results['score'] = results['score'].apply(ast.literal_eval)
results['winner'] = [x['winner'] for x in results['score']]
results['homeScore'] = [x['fullTime']['homeTeam'] for x in results['score']]
results['awayScore'] = [x['fullTime']['awayTeam'] for x in results['score']]

results = results[['matchday','homeTeam','awayTeam',
                   'homeScore','awayScore','winner']]

teams = results.homeTeam.unique()

table = pd.DataFrame(0, index=teams,
                     columns=['Pld','W','D','L','GF','GA','GD','Pts',
                              'HPld','HW','HD','HL','HGF','HGA','HGD','HPts',
                              'APld','AW','AD','AL','AGF','AGA','AGD','APts'])

for team in teams:
    home = results[results.homeTeam==team]
    table.loc[team,'HPld'] = len(home)
    table.loc[team,'HW'] = (home['winner']=='HOME_TEAM').sum()
    table.loc[team,'HD'] = (home['winner']=='DRAW').sum()
    table.loc[team,'HL'] = (home['winner']=='AWAY_TEAM').sum()
    table.loc[team,'HGF'] = home['homeScore'].sum()
    table.loc[team,'HGA'] = home['awayScore'].sum()
    
    away = results[results.awayTeam==team]
    table.loc[team,'APld'] = len(home)
    table.loc[team,'AW'] = (away['winner']=='AWAY_TEAM').sum()
    table.loc[team,'AD'] = (away['winner']=='DRAW').sum()
    table.loc[team,'AL'] = (away['winner']=='HOME_TEAM').sum()
    table.loc[team,'AGF'] = away['awayScore'].sum()
    table.loc[team,'AGA'] = away['homeScore'].sum()

table['HGD'] = table['HGF']-table['HGA']
table['HPts'] = 3*table['HW']+table['HD'] 

table['AGD'] = table['AGF']-table['AGA']
table['APts'] = 3*table['AW']+table['AD']

table['Pld'] = table['HPld']+table['APld']
table['W'] = table['HW']+table['AW']
table['D'] = table['HD']+table['AD']
table['L'] = table['HL']+table['AL']
table['GF'] = table['HGF']+table['AGF']
table['GA'] = table['HGA']+table['AGA']
table['GD'] = table['HGD']+table['AGD']
table['Pts'] = table['HPts']+table['APts']

print(table[['HPld','HW','HD','HL','HGF','HGA','HGD','HPts']].sort_values(by=['HPts','HGD','HGF'],ascending=False))