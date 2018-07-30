import pandas as pd
import numpy as np

import scipy.optimize as scopt
import matplotlib.pyplot as plt

results = pd.read_csv('processed/results.csv')

hTeam,teams = results['homeTeam'].factorize(sort=True)
aTeam,_ = results['awayTeam'].factorize(sort=True)
n_teams = len(teams)

hScore = results['homeScore'].values
aScore = results['awayScore'].values

x = np.ones(4*n_teams)

def get_k(x):
    k_home_score = x[:n_teams]
    k_away_score = x[n_teams:(2*n_teams)]
    k_home_concede = x[(2*n_teams):(3*n_teams)]
    k_away_concede = x[(3*n_teams):]

    return (k_home_score,k_away_score,
            k_home_concede,k_away_concede)
    
def predict_home(k_home_score,k_away_concede):
    return k_home_score[hTeam]*k_away_concede[aTeam]

def predict_away(k_away_score,k_home_concede):
    return k_away_score[aTeam]*k_home_concede[hTeam]


def f(x):
    (k_home_score,k_away_score,k_home_concede,k_away_concede) = get_k(x) 
    
    hPred = predict_home(k_home_score,k_away_concede)
    aPred = predict_away(k_away_score,k_home_concede)

    hErr = (hScore - hPred)**2
    aErr = (aScore - aPred)**2
    
    return sum(hErr+aErr)

result = scopt.least_squares(f, x, bounds=(0,4))
x = result.x
(k_home_score,k_away_score,k_home_concede,k_away_concede) = get_k(x)

result_df = pd.DataFrame({'home_score':k_home_score,'away_score':k_away_score,
                          'home_concede':k_home_concede,'away_concede':k_away_concede},
                         index=teams)

(k_home_score,k_away_score,k_home_concede,k_away_concede) = get_k(x)
pred_a = predict_away(k_away_score,k_home_concede)
pred_h = predict_home(k_home_score,k_away_concede)

preds = results[['homeTeam','awayTeam','homeScore','awayScore','winner']].copy()
preds['homePred'] = pred_h
preds['awayPred'] = pred_a

preds['homeErr'] = preds['homeScore']-preds['homePred']
preds['awayErr'] = preds['awayScore']-preds['awayPred']

def predict_winner(row):
    if row['homePred']-row['awayPred']>0.5:
        return 'HOME_TEAM'
    elif row['homePred']-row['awayPred']<-0.5:
        return 'AWAY_TEAM'
    else:
        return 'DRAW'
    
preds['pred_winner'] = preds.apply(predict_winner,axis=1)

print(preds.groupby('winner').pred_winner.value_counts(normalize=True))
print('fraction of correct predictions:',(preds['winner']==preds['pred_winner']).mean())

def winner_error(row):
    if row['winner']==row['pred_winner']:
        return 0
    
    elif row['winner']=='HOME_TEAM' and row['pred_winner']=='DRAW':
        return 1
    
    elif row['winner']=='AWAY_TEAM' and row['pred_winner']=='DRAW':
        return 1
    
    elif row['winner']=='DRAW' and row['pred_winner']=='HOME_TEAM':
        return 1
    
    elif row['winner']=='DRAW' and row['pred_winner']=='AWAY_TEAM':
        return 1
    
    elif row['winner']=='HOME_TEAM' and row['pred_winner']=='AWAY_TEAM':
        return 2
    
    elif row['winner']=='AWAY_TEAM' and row['pred_winner']=='HOME_TEAM':
        return 2
       
    else:
        print('ERROR',row['winner'],row['pred_winner'])
        
print('mean result error:',preds.apply(winner_error,axis=1).mean())
print('mean home goals error:',preds['homeErr'].abs().mean())
print('mean away goals error:',preds['awayErr'].abs().mean())

plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
preds['homeErr'].plot.hist()
plt.title('home goals error')
plt.subplot(1,2,2)
preds['awayErr'].plot.hist()
plt.title('away goals error')
plt.show()