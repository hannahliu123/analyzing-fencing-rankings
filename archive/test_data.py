from load_csv import tournament_df, bout_df, fencer_bio_df, fencer_rankings_df

print("Tournaments:", tournament_df.shape)
print("Bouts:", bout_df.shape)
print("Fencer bios:", fencer_bio_df.shape)
print("Fencer rankings:", fencer_rankings_df.shape)

print("\n--- TOURNAMENTS ---")
print(tournament_df.head())

print("\n--- BOUTS ---")
print(bout_df.head())

print("\n--- FENCER BIOS ---")
print(fencer_bio_df.head())

print("\n--- MISSING DATA FLAGS ---")
print(tournament_df['missing_results_flag'].value_counts())
