import pandas as pd

date = 'Jun_30_2026'
div_name = 'all_mens_foil'

bout_df            = pd.read_csv('output/'+date+'/'+div_name+ '_bout_data_'            +date+'.csv')
tournament_df      = pd.read_csv('output/'+date+'/'+div_name+ '_tournament_data_'      +date+'.csv')

bout_df = bout_df.merge(
    tournament_df[['unique_ID', 'category']],
    left_on='tournament_ID',
    right_on='unique_ID',
    how='left'
).drop(columns=['unique_ID'])   # we don't need this cos it's the same as tournament_ID

bout_df.to_csv(f'output/{date}/{div_name}_bout_data_{date}.csv', index=False)

print("DONE adding category column!")
