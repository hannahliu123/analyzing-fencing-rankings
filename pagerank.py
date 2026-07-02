# this script creates the graph with networkx and runs the pagerank algorithm to create a new csv file for pagerank
# the only factor impacting edge weight is the round (pool or DE)

import networkx as nx
import pandas as pd
import os
from operator import itemgetter

date = 'Jun_30_2026'
div_name = 'all_mens_foil'
weapon = "Foil"
gender = "Mens"

bout_df            = pd.read_csv('output/'+date+'/'+div_name+ '_bout_data_'            +date+'.csv')
fencer_bio_df      = pd.read_csv('output/'+date+'/'+div_name+ '_fencer_bio_data_'      +date+'.csv')

pagerank_records = []   # scores and rankings for all fecners in each season

for (season, category), season_df in bout_df.groupby(['season', 'category']):
    print(f"--- Processing Season: {season} for the category (age group): {category} ---")
    season_records = [] # scores and rankings for all fencers this season & age
    G = nx.DiGraph()

    for bout in season_df.itertuples():
        winner_id = bout.winner_ID
        loser_id  = bout.fencer_ID if bout.winner_ID == bout.opp_ID else bout.opp_ID

        # decide on a weighting scheme
        if bout.bout_type == "pool": weight = 0.2
        else: weight = 1.0

        # edge already exists
        if G.has_edge(loser_id, winner_id):
            G[loser_id][winner_id]['weight'] += weight
        else:
            G.add_edge(loser_id, winner_id, weight=weight)
    
    # mess with alpha
    scores = nx.pagerank(G, alpha=0.85, weight='weight')
    sorted_fencers = sorted(scores.items(), key=itemgetter(1), reverse=True)    # g -> l

    # add to pagerank_records
    for rank, (fencer_id, score) in enumerate(sorted_fencers, start=1):
        names = fencer_bio_df.loc[fencer_bio_df['id'] == fencer_id, 'name']
        name = names.item() if not names.empty else "N/A"
        pagerank_records.append({
            'id': fencer_id, 'name': name, 'season': season, 'category': category,
            'weapon': weapon, 'gender': gender, 'pagerank_score': score, 'pagerank_rank':  rank
        })

# cumulative records
cumulative_path = 'data_analysis/all_pagerank_rankings.csv'
pagerank_df = pd.DataFrame(pagerank_records)
if os.path.exists(cumulative_path):
    existing = pd.read_csv(cumulative_path)
    combined = pd.concat([existing, pagerank_df], ignore_index=True)
    combined = combined.drop_duplicates(
        subset=['id', 'season', 'category', 'weapon', 'gender'], keep='last'
    )
    combined.to_csv(cumulative_path, index=False)
    print(f"Appended {len(pagerank_df)} records → {cumulative_path} now has {len(combined)} total")
else:
    pagerank_df.to_csv(cumulative_path, index=False)
    print(f"Created {cumulative_path} with {len(pagerank_df)} records")
