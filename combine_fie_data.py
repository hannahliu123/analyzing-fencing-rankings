# Reads fencer_rankings_data CSVs for all 6 divisions and combines them into one flat CSV at data_analysis/all_fie_rankings.csv

import pandas as pd
import os

divisions = [
    ('all_womens_foil',  'Foil',  'Womens', 'Jun_25_2026'),
    ('all_womens_epee',  'Epee',  'Womens', 'Jun_27_2026'),
    ('all_womens_sabre', 'Sabre', 'Womens', 'Jun_26_2026'),
    ('all_mens_foil',    'Foil',  'Mens',   'Jun_30_2026'),
    ('all_mens_epee',    'Epee',  'Mens',   'Jun_29_2026'),
    ('all_mens_sabre',   'Sabre', 'Mens',   'Jun_28_2026'),
]

all_records = []
for div_name, weapon, gender, date in divisions:
    path = f'output/{date}/{div_name}'
    
    rankings_path = path + f'_fencer_rankings_data_{date}.csv'
    bio_path      = path + f'_fencer_bio_data_{date}.csv'
    
    if not os.path.exists(rankings_path):
        print(f"Skipping {div_name} — file not found")
        continue
    
    # id, weapon, category, season, rank, points
    rankings_df = pd.read_csv(rankings_path, index_col=[0, 1, 2, 3])
    rankings_flat = rankings_df.reset_index()
    bio_df      = pd.read_csv(bio_path)
    
    # fix season labels: stored as "X/X+1" but should be "X-1/X"
    rankings_flat['season'] = rankings_flat['season'].apply(
        lambda s: f"{int(s.split('/')[0])-1}/{int(s.split('/')[1])-1}"
    )
    
    merged = rankings_flat.merge(
        bio_df[['id', 'name', 'country']], on='id', how='left'
    )
    merged['gender'] = gender
    
    all_records.append(merged)
    print(f"Loaded {len(merged)} records from {div_name}")

# combine all divisions
combined = pd.concat(all_records, ignore_index=True)
combined = combined.drop_duplicates(subset=['id', 'weapon', 'category', 'season'])
combined = combined.rename(columns={
    'rank':   'fie_rank',
    'points': 'fie_score'
})
combined = combined[[
    'id', 'name', 'country', 'weapon', 'gender', 'category', 'season', 
    'fie_score', 'fie_rank'
]]

combined = combined.sort_values(['weapon', 'gender', 'category', 'season', 'fie_rank'])

combined.to_csv('data_analysis/all_fie_rankings.csv', index=False)
print(f"\nSaved {len(combined)} total FIE ranking records")
