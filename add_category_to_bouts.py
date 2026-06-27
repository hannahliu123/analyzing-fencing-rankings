from load_csv import tournament_df, bout_df, date, div_name

bout_df = bout_df.merge(
    tournament_df[['unique_ID', 'category']],
    left_on='tournament_ID',
    right_on='unique_ID',
    how='left'
).drop(columns=['unique_ID'])   # we don't need this cos it's the same as tournament_ID

bout_df.to_csv(f'output/{date}/{div_name}_bout_data_{date}.csv', index=False)

print(bout_df.columns.tolist())  # verify category is there
print(bout_df['category'].value_counts())  # verify it populated correctly
