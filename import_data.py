#################
### VARIABLES ###
#################
update_api = True
###
FPL_URL = 'https://fantasy.premierleague.com/drf/bootstrap-static'
FOOTDATA_URL = 'http://api.football-data.org/v2/competitions/2021/'
LAST_SEASON_START = '2017-06-01'
LAST_SEASON_STOP = '2018-06-01'
###
fpl_file = 'json/fpl.json'
fixtures_file = 'json/fixtures.json'
results_file = 'json/results.json'
standings_file = 'json/standings.json'
token_file = 'api.token'

###############
### IMPORTS ###
###############
import requests
import json
import pandas as pd

#################
### FUNCTIONS ###
#################
def get_json(url,headers=[]):
    print('Getting',url,'...')
    raw = requests.get(url, headers=headers)
    print(type(raw))
    raw_json = raw.json()
    return raw_json

def save_json(raw_json, fname):
    print('Saving',fname,'...')
    with open(fname, 'w') as f:
        json.dump(raw_json, f)
        
def load_json(fname):
    print('Loading',fname,'...')
    with open(fname, 'r') as f:
        raw_json = f.read()
    
    # convert to dict
    raw_json = json.loads(raw_json)
    
    return raw_json
  
def json_to_df(raw_json,prefix='',suffix='.csv'):  
    print('Converting json to data frames:')
    for key in raw_json.keys():
        print(key+'...', end='')
        try:
            df = pd.DataFrame(raw_json[key])
            df.to_csv(prefix + key + suffix, index=False)
            print('done.')
        except:
            try:
                df = pd.Series(raw_json[key])
                df.to_csv(prefix + key + suffix, index=True)
                print('done.')
            except:
                print('ERROR!')
            
################
### FPL DATA ###
################            
if update_api:
    raw_json = get_json(FPL_URL)
    save_json(raw_json, fpl_file)    
    
else:
    raw_json = load_json(fpl_file)

print('------------------')
json_to_df(raw_json,prefix='json/FPL_')

##################################################################
### FIXTURE DATA (all fixtures and results for current season) ###
##################################################################   
print('------------------')

if update_api:
    with open(token_file,'r') as f:
        token = f.read()
        
    raw_json = get_json(FOOTDATA_URL+'matches',
                        headers={'X-Auth-Token':token})
    
    save_json(raw_json, fixtures_file)    
    
else:
    raw_json = load_json(fixtures_file)

print('------------------')
json_to_df(raw_json,prefix='json/Fixtures_')

##################################################################
### RESULTS DATA (all results for last season) ###
##################################################################   

print('------------------')
if update_api:
    url = FOOTDATA_URL+'matches?dateFrom='+LAST_SEASON_START+'&dateTo='+LAST_SEASON_STOP
    raw_json = get_json(url, headers={'X-Auth-Token':token})
    
    save_json(raw_json, results_file)    
    
else:
    raw_json = load_json(results_file)

print('------------------')
json_to_df(raw_json,prefix='json/Results_')

######################
### STANDINGS DATA ###
######################      
      
print('------------------')
if update_api:
    raw_json = get_json(FOOTDATA_URL+'standings',
                        headers={'X-Auth-Token':token})
    
    save_json(raw_json, standings_file)    
    
else:
    raw_json = load_json(standings_file)

print('------------------')
json_to_df(raw_json,prefix='json/Standings_')