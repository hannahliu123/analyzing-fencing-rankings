# Create data_analysis/all_sensitivity_results.csv (only for Senior category) ----------------------

import pandas as pd
import networkx as nx
import os
from operator import itemgetter
from scipy.stats import spearmanr

divisions = [
    ('all_womens_foil',  'Foil',  'Womens', 'Jun_25_2026'),
    ('all_womens_epee',  'Epee',  'Womens', 'Jun_27_2026'),
    ('all_womens_sabre', 'Sabre', 'Womens', 'Jun_26_2026'),
    ('all_mens_foil',    'Foil',  'Mens',    'Jun_30_2026'),
    ('all_mens_epee',    'Epee',  'Mens',   'Jun_29_2026'),
    ('all_mens_sabre',   'Sabre', 'Mens',   'Jun_28_2026'),
]

configs = [
    {'pool': 0.1, 'de': 1.0, 'alpha': 0.85},
    {'pool': 0.5, 'de': 1.0, 'alpha': 0.85},
    {'pool': 1.0, 'de': 1.0, 'alpha': 0.85},
    {'pool': 0.2, 'de': 1.0, 'alpha': 0.90},
]

baseline_df = pd.read_csv('data_analysis/all_pagerank_rankings.csv')
sensitivity_records = []

for div_name, weapon, gender, date in divisions:
    print(f"\n--- {weapon} {gender} ---")
    path     = f'output/{date}/{div_name}'
    bout_df  = pd.read_csv(path + f'_bout_data_{date}.csv')
    bout_df = bout_df[bout_df['category'] == 'Senior']  # Senior only
    
    for config in configs:
        pool_w = config['pool']
        alpha  = config['alpha']
        print(f"Running config: pool weight={pool_w}, alpha={alpha}")

        for season, season_df in bout_df.groupby('season'):
            # build graph for season, Senior, weapon, gender with this config
            G = nx.DiGraph()
            for bout in season_df.itertuples():
                winner_id = bout.winner_ID
                loser_id  = bout.fencer_ID if bout.winner_ID == bout.opp_ID else bout.opp_ID
                weight = pool_w if bout.bout_type == 'pool' else 1.0
                if G.has_edge(loser_id, winner_id):
                    G[loser_id][winner_id]['weight'] += weight
                else:
                    G.add_edge(loser_id, winner_id, weight=weight)
            
            scores = nx.pagerank(G, alpha=alpha, weight='weight')
            config_ranks = pd.DataFrame([
                {'id': fid, 'config_rank': rank}
                for rank, (fid, _) in enumerate(    # loop trop g->l scores starting from rank=1
                    sorted(scores.items(), key=itemgetter(1), reverse=True), 1)
            ])
            
            # get baseline rankings for this season/weapon/gender/Senior
            fie_season = f"{int(season)-1}/{int(season)}"
            baseline_group = baseline_df[
                (baseline_df['season']   == season) &
                (baseline_df['weapon']   == weapon) &
                (baseline_df['gender']   == gender) &
                (baseline_df['category'] == 'Senior')
            ][['id', 'pagerank_rank']]
            
            if len(baseline_group) < 10: continue
            merged = baseline_group.merge(config_ranks, on='id')
            if len(merged) < 10: continue
            
            rho, _ = spearmanr(merged['pagerank_rank'], merged['config_rank'])
            
            sensitivity_records.append({
                'weapon':          weapon,
                'gender':          gender,
                'season':          fie_season,
                'category':        'Senior',
                'pool_weight':     pool_w,
                'alpha':           alpha,
                'rho_vs_baseline': round(rho, 4),
                'n_fencers':       len(merged)
            })

sensitivity_df = pd.DataFrame(sensitivity_records)
cumulative_path = 'data_analysis/all_sensitivity_results.csv'
sensitivity_df.to_csv(cumulative_path, index=False)
print(f"Saved {len(sensitivity_df)} rows to {cumulative_path}")


# Interpret Sentitivity Test Results -----------------------------------------------------------
print("\n=== SENSITIVITY SUMMARY ===")
summary = sensitivity_df.groupby(['pool_weight', 'alpha'])['rho_vs_baseline'].agg(
    mean='mean', min='min', max='max'
).round(4)

print(summary)
