# builds TrueSkill ratings for each fencer per season and category and adds to all_trueskill_rankings.csv
# run once per weapon/gender division 

import trueskill
import pandas as pd
import os
from operator import itemgetter

date = 'Jun_25_2026'
div_name = 'all_womens_foil'
weapon = "Foil"
gender = "Womens"

bout_df = pd.read_csv('output/'+date+'/'+div_name+ '_bout_data_' +date+'.csv')
fencer_bio_df = pd.read_csv('output/'+date+'/'+div_name+ '_fencer_bio_data_' +date+'.csv')

env = trueskill.TrueSkill(
    mu=25.0,        # default starting skill
    sigma=8.333,    # default starting uncertainty (mu/3)
    beta=4.167,     # performance variability (how much randomness per bout)
    tau=0.083,      # dynamic factor (how much ratings drift over time)
    draw_probability=0.0    # no draws in fencing
)
trueskill_records = []   # scores and rankings for all fencers in each season

for (season, category), season_df in bout_df.groupby(['season', 'category']):
    print(f"--- Processing Season: {season} for the category (age group): {category} ---")
    season_df = season_df.sort_values('date').reset_index(drop=True)
    ratings = {}    # fencer_id: trueskill.Rating

    for bout in season_df.itertuples():
        winner_id = bout.winner_ID
        loser_id = bout.fencer_ID if bout.winner_ID == bout.opp_ID else bout.opp_ID

        # current ratings
        r_winner = ratings.get(winner_id, env.create_rating())
        r_loser = ratings.get(loser_id, env.create_rating())
        
        # update ratings based on result
        new_winner, new_loser = env.rate_1vs1(r_winner, r_loser)
        ratings[winner_id] = new_winner
        ratings[loser_id] = new_loser
    
    # rank all fencers with compute all four scoring variants
    scores = []
    for fencer_id, r in ratings.items():
        scores.append({
            'fencer_id': fencer_id, 
            'mu': r.mu, 'sigma': r.sigma,
            'ts_score_3sigma': r.mu - 3 * r.sigma,   # standard
            'ts_score_2sigma': r.mu - 2 * r.sigma,
            'ts_score_1sigma': r.mu - 1 * r.sigma,
            'ts_score_mu': r.mu
        })
    
    # sort by each variant to assign ranks
    for variant in ['ts_score_3sigma', 'ts_score_2sigma', 'ts_score_1sigma', 'ts_score_mu']:
        scores.sort(key=itemgetter(variant), reverse=True)
        for rank, s in enumerate(scores, start=1):
            s[f'rank_{variant}'] = rank     # for all fencers, add rank under each variant
    
    name_lookup = dict(zip(fencer_bio_df['id'], fencer_bio_df['name']))
    for s in scores:
        fid = s['fencer_id']
        name = name_lookup.get(fid, 'Unknown')
        trueskill_records.append({
            'id': fid, 'name': name, 'season': season, 
            'category': category, 'weapon': weapon, 'gender': gender,
            'mu': round(s['mu'], 4), 'sigma': round(s['sigma'], 4),
            'ts_score_3sigma': round(s['ts_score_3sigma'], 4),
            'ts_score_2sigma': round(s['ts_score_2sigma'], 4),
            'ts_score_1sigma': round(s['ts_score_1sigma'], 4),
            'ts_score_mu': round(s['ts_score_mu'], 4),
            'ts_rank_3sigma': s['rank_ts_score_3sigma'],
            'ts_rank_2sigma': s['rank_ts_score_2sigma'],
            'ts_rank_1sigma': s['rank_ts_score_1sigma'],
            'ts_rank_mu': s['rank_ts_score_mu']
        })

trueskill_df = pd.DataFrame(trueskill_records)
trueskill_df['fie_season'] = trueskill_df['season'].apply(
    lambda s: f"{int(s)-1}/{int(s)}"
)

cumulative_path = 'data_analysis/all_trueskill_rankings.csv'
if os.path.exists(cumulative_path):
    existing = pd.read_csv(cumulative_path)
    combined = pd.concat([existing, trueskill_df], ignore_index=True)
    combined = combined.drop_duplicates(
        subset=['id', 'season', 'category', 'weapon', 'gender'], keep='last'
    )
    combined.to_csv(cumulative_path, index=False)
    print(f"Appended → {cumulative_path} now has {len(combined)} rows")
else:
    trueskill_df.to_csv(cumulative_path, index=False)
    print(f"Created {cumulative_path} with {len(trueskill_df)} rows")
