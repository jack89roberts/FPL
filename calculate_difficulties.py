import pandas as pd
import ast
import matplotlib.pyplot as plt

#TEST

fixtures = pd.read_csv('processed/fixtures.csv',index_col='matchday')
# convert strings to tuples
fixtures = fixtures.applymap(ast.literal_eval) 

strengths = pd.read_csv('processed/strengths.csv',index_col='Team')

def difficulty_attack(fixture):
    team = fixture[0]
    stadium = fixture[1]
    
    if stadium=='Home':
        #def_diff = strengths.loc[team,'A_Att']
        att_diff = strengths.loc[team,'A_Def']
    else:
        #def_diff = strengths.loc[team,'H_Att']
        att_diff = strengths.loc[team,'H_Def']
        
    return att_diff

def difficulty_defence(fixture):
    team = fixture[0]
    stadium = fixture[1]
    
    if stadium=='Home':
        def_diff = strengths.loc[team,'A_Att']
    else:
        def_diff = strengths.loc[team,'H_Att']
        
    return def_diff

att_diff = fixtures.applymap(difficulty_attack)
def_diff = fixtures.applymap(difficulty_defence)

plt.plot(att_diff['Chelsea'])
plt.plot(def_diff['Chelsea'])
plt.show()


