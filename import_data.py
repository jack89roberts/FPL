#################
### VARIABLES ###
#################
update_api = False
fpl_file = 'json/fpl.json'
fixtures_file = 'json/fixtures.json'
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
            print('ERROR!')
            
################
### FPL DATA ###
################            
if update_api:
    raw_json = get_json('https://fantasy.premierleague.com/drf/bootstrap-static')
    save_json(raw_json, fpl_file)    
    
else:
    raw_json = load_json(fpl_file)

print('------------------')
json_to_df(raw_json,prefix='json/FPL_')

####################
### FIXTURE DATA ###
####################            
print('------------------')

if update_api:
    with open(token_file,'r') as f:
        token = f.read()
        
    raw_json = get_json('http://api.football-data.org/v2/competitions/2021/matches',
                        headers={'X-Auth-Token':token})
    
    save_json(raw_json, fixtures_file)    
    
else:
    raw_json = load_json(fixtures_file)

print('------------------')
json_to_df(raw_json,prefix='json/Fixtures_')