import requests
import json
import pandas as pd

update_file = False
file_name = 'raw.json'

if update_file:
    raw = requests.get('https://fantasy.premierleague.com/drf/bootstrap-static')
    raw_json = raw.json()
    
    with open(file_name,'w') as dump_file:
        json.dump(raw_json, dump_file)
        
else:
    with open(file_name, 'r') as dump_file:
        raw_json = dump_file.read() 

json_dict = json.loads(raw_json)

for key in json_dict.keys():
    print(key+'...', end='')
    try:
        df = pd.DataFrame(json_dict[key])
        df.to_csv(key+'.csv')
        print('done.')
    except:
        print('ERROR!')

