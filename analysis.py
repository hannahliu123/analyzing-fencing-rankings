from scipy.stats import spearmanr
import pandas as pd
import matplotlib.pyplot as plt

ts_df = pd.read_csv('data_analysis/all_trueskill_rankings.csv')
pagerank_df = pd.read_csv('data_analysis/all_pagerank_rankings.csv')
fie_df = pd.read_csv('data_analysis/all_fie_rankings.csv')

region_colors = {
    'Europe':            '#4575b4',
    'Asia':              '#d73027',
    'Americas':          '#1a9850',
    'Africa/Middle East':'#fdae61',
    'Other':             '#bababa',
}

sigma_colors = {
    0: "#7F7F7F",
    1: '#d73027',
    2: "#ff8000",
    3: "#ffd900",
}

def get_region(country):
    europe = [
        '_A', 'A_', 'FRANCE', 'ITALY', 'HUNGARY', 'RUSSIA', 'UKRAINE', 'GERMANY',
        'POLAND', 'ROMANIA', 'GREECE', 'SPAIN', 'BULGARIA', 'BELARUS',
        'GEORGIA', 'AZERBAIJAN', 'TURKEY', 'SERBIA', 'CROATIA',
        'CZECH REPUBLIC', 'SLOVAKIA', 'AUSTRIA', 'SWITZERLAND',
        'BELGIUM', 'NETHERLANDS', 'SWEDEN', 'NORWAY', 'DENMARK',
        'FINLAND', 'PORTUGAL', 'GREAT BRITAIN', 'ESTONIA', 'LATVIA',
        'LITHUANIA', 'MOLDOVA', 'ARMENIA', 'LUXEMBOURG', 'IRELAND',
        'SLOVENIA', 'NORTH MACEDONIA', 'ALBANIA', 'ICELAND',
        'BOSNIA AND HERZEGOVINA', 'CYPRUS', 'MALTA', 'MONTENEGRO',
        'ANDORRA', 'SAN MARINO', 'LIECHTENSTEIN'
    ]
    asia = [
        'CHINA', 'KOREA', 'JAPAN', 'KAZAKHSTAN', 'UZBEKISTAN', 
        'IRAN', 'HONG KONG', 'HONG KONG, CHINA', 'CHINESE TAIPEI',
        'MONGOLIA', 'INDIA', 'THAILAND', 'SINGAPORE', 'MALAYSIA',
        'PHILIPPINES', 'INDONESIA', 'VIETNAM', 'KYRGYZSTAN',
        'TAJIKISTAN', 'TURKMENISTAN', 'BANGLADESH', 'SRI LANKA',
        'PAKISTAN', 'AFGHANISTAN', 'CAMBODIA', 'MYANMAR', 'NEPAL',
        'NEW ZEALAND', 'AUSTRALIA', 'BRUNEI DARUSSALAM', "MACAO, CHINA"
    ]
    americas = [
        'UNITED STATES', 'UNITED STATES OF AMERICA', 'USA',
        'CANADA', 'BRAZIL', 'MEXICO', 'ARGENTINA', 'CUBA',
        'VENEZUELA', 'COLOMBIA', 'PERU', 'CHILE', 'ECUADOR',
        'PANAMA', 'DOMINICAN REPUBLIC', 'TRINIDAD AND TOBAGO',
        'PUERTO RICO', 'URUGUAY', 'PARAGUAY', 'BOLIVIA',
        'COSTA RICA', 'GUATEMALA', 'HONDURAS', 'EL SALVADOR',
        'NICARAGUA', 'JAMAICA', 'BARBADOS', 'HAITI', 'GUYANA',
        'SURINAME', 'BELIZE'
    ]
    africa_me = [
        # North Africa
        'EGYPT', 'ALGERIA', 'TUNISIA', 'MOROCCO', 'LIBYA', 'SUDAN',
        # Sub-Saharan Africa
        'SENEGAL', 'SOUTH AFRICA', 'NIGERIA', 'GHANA', 'CAMEROON',
        'IVORY COAST', "COTE D'IVOIRE", 'MADAGASCAR', 'KENYA',
        'ETHIOPIA', 'TANZANIA', 'UGANDA', 'ZIMBABWE', 'ZAMBIA',
        'MOZAMBIQUE', 'ANGOLA', 'NAMIBIA', 'BOTSWANA', 'TOGO',
        'BENIN', 'MALI', 'BURKINA FASO', 'NIGER', 'CHAD',
        'DEMOCRATIC REPUBLIC OF CONGO', 'REPUBLIC OF CONGO',
        'RWANDA', 'BURUNDI', 'SOMALIA', 'ERITREA', 'DJIBOUTI',
        'MAURITIUS', 'SEYCHELLES', 'CAPE VERDE', 'GAMBIA',
        'GUINEA', 'GUINEA-BISSAU', 'SIERRA LEONE', 'LIBERIA',
        # Middle East
        'SAUDI ARABIA', 'UAE', 'UNITED ARAB EMIRATES', 'QATAR',
        'KUWAIT', 'BAHRAIN', 'IRAQ', 'JORDAN', 'LEBANON',
        'SYRIA', 'ISRAEL', 'PALESTINE', 'OMAN', 'YEMEN'
    ]
    
    if country in europe:   return 'Europe'
    if country in asia:     return 'Asia'
    if country in americas: return 'Americas'
    if country in africa_me: return 'Africa/Middle East'
    print(f"country {country} resulted in an invlaid region")
    return 'Other'

def make_scatter(ax, df, lim, title, rank, rank_name, label_these, use_region):
    if use_region==2:   # based on sigma
        df = df.copy()
        for sigma_cat, group in df.groupby('sigma_category'):
            print(f"the sigma category {sigma_cat} exists with color {sigma_colors[sigma_cat]}")
            ax.scatter(
                group['fie_rank'], group[rank],
                alpha=0.5, s=20, color=sigma_colors[sigma_cat], label=sigma_cat
            )
    elif use_region==1:   # based on region
        df = df.copy()
        df['region'] = df['country'].apply(get_region)
        for region, group in df.groupby('region'):
            ax.scatter(
                group['fie_rank'], group[rank],
                alpha=0.5, s=20, color=region_colors[region], label=region
            )
    else:
        ax.scatter(
            df['fie_rank'], df[rank],
            alpha=0.5, s=20, color='steelblue'
        )

    ax.plot([1, lim-lim/150], [1, lim-lim/150],   # diagonal line
            color='red', linestyle='--', linewidth=1, alpha=0.7, label='Perfect agreement')
    
    for _, row in df.iterrows():
        name = row['name']
        if name in label_these:
            last_name = name.split()[0]
            if last_name == "DI": last_name = "DI CARLO"    # heh shhh
            ax.annotate(
                last_name,
                xy=(row['fie_rank'], row[rank]),
                xytext=(row['fie_rank'] + lim/110, row[rank] - lim/140),
                fontsize=7, alpha=0.8, fontweight='bold'
            )
    
    ax.set_xlim(-lim/100, lim)
    ax.set_ylim(-lim/100, lim)
    ax.set_xlabel('Official FIE Rank', fontsize=11)
    ax.set_ylabel(f'{rank_name} Rank', fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.legend(loc='lower right', fontsize=9)
    ax.text(
        0.02, 0.98, 'Note: Smaller rank values indicate stronger skill\nEx. Rank #1 = Best',
        transform=ax.transAxes, fontsize=9, color='gray', style='italic', ha='left', va='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='lightgray', alpha=0.8)
    )
    
    ax.grid(alpha=0.2)
    print(f"Finished plotting {len(df)} fencers with {rank_name}")


# Create data_analysis/all_pagerank_trueskill_fie_comparisons.csv --------------------------------------------
comparison_records = []
for (weapon, gender, category, season), group in pagerank_df.groupby(
    ['weapon', 'gender', 'category', 'season']):
    
    fie_season = f"{str(season-1)}/{str(season)}"
    fie = fie_df[
        (fie_df['season']   == fie_season) &
        (fie_df['weapon']   == weapon) &
        (fie_df['gender']   == gender) &
        (fie_df['category'] == category)
    ][['id', 'fie_rank', 'fie_score', 'name', 'country', 'weapon', 'gender', 'category', 'season']]
    pr = group[['id', 'pagerank_rank', 'pagerank_score']].copy()
    
    # id, name, country, season, weapon, gender, category, pagerank_rank, pagerank_score, fie_rank, fie_score, rank_diff, abs_diff
    merged = pr.merge(fie, on='id', how='inner')
    merged['rank_diff'] = merged['fie_rank'] - merged['pagerank_rank']
    merged['abs_diff'] = merged['rank_diff'].abs()
    
    comparison_records.append(merged)

comparison_df = pd.concat(comparison_records, ignore_index=True)

ts_cols = ts_df[['id', 'fie_season', 'weapon', 'gender', 'category', 'mu', 'sigma',
                'ts_rank_mu', 'ts_rank_1sigma', 'ts_rank_2sigma', 'ts_rank_3sigma']].copy()
comparison_df = comparison_df.merge(
    ts_cols,
    left_on = ['id', 'season', 'weapon', 'gender', 'category'],
    right_on = ['id', 'fie_season', 'weapon', 'gender', 'category'],
    how ='left'
).drop(columns=['fie_season'])
comparison_df['ts_rank_diff'] = comparison_df['fie_rank'] - comparison_df['ts_rank_1sigma']
comparison_df['ts_abs_diff'] = comparison_df['ts_rank_diff'].abs()
comparison_df['sigma_category'] = pd.cut(
    comparison_df['sigma'],
    bins=[0, 1, 3, 5, float('inf')],
    labels=[0, 1, 2, 3]
).astype(int)

comparison_df = comparison_df[[
    'id', 'name', 'country', 'season', 'weapon', 'gender', 'category',
    'pagerank_rank', 'pagerank_score', 'fie_rank', 'fie_score', 'rank_diff', 'abs_diff',
    'mu', 'sigma', 'sigma_category',
    'ts_rank_mu', 'ts_rank_1sigma', 'ts_rank_2sigma', 'ts_rank_3sigma', 'ts_rank_diff', 'ts_abs_diff'
]]
comparison_df.to_csv('data_analysis/all_pagerank_trueskill_fie_comparisons.csv', index=False)
print(f"Saved {len(comparison_df)} comparison records")


# Create scatterplot from all_pagerank_fie_comparisons.csv -----------------------------------------
sabre_2025 = comparison_df[
    (comparison_df['weapon']   == 'Sabre') &
    (comparison_df['category'] == 'Senior') &
    (comparison_df['season']   == '2024/2025')
].copy()
womens = sabre_2025[sabre_2025['gender'] == 'Womens'].copy()
mens = sabre_2025[sabre_2025['gender'] == 'Mens'].copy()


# Decide who to do case studies on
pr_or_ts = 'ts_rank_1sigma'     # pagerank_rank or ts_rank_1sigma
diff = 'ts_rank_diff'      # rank_diff or ts_rank_diff
abs = 'ts_abs_diff'     # abs_diff or ts_abs_diff
womens_notable = womens[
    ((womens[pr_or_ts] <= 100) | (womens['fie_rank'] <= 100)) & (womens[abs] >= 50)
].sort_values(abs, ascending=False)
mens_notable = mens[
    ((mens[pr_or_ts] <= 150) | (mens['fie_rank'] <= 150)) & (mens[abs] >= 50)
].sort_values(abs, ascending=False)
print("\n=== WOMENS SABRE SENIOR 2024/2025 — Top 64 Notable Divergences ===")
print(womens_notable[['name', pr_or_ts, 'fie_rank', diff, abs]].to_string(index=False))
print("\n=== MENS SABRE SENIOR 2024/2025 — Top 64 Notable Divergences ===")
print(mens_notable[['name', pr_or_ts, 'fie_rank', diff, abs]].to_string(index=False))

womens_labels = [
    'BOUAJINA Aicha', 'REZGUI Yesmine', 'ELDOKSH Renad ',   # way far up
    'KEHLI Zohra Nora', 'BENADOUDA Chaima ', 'HAFEZ Nada', 'HEGAZY Alanoud', 'CARVALHO Isabela',
    'WEI Jiayi', 'KIKUCHI Kokona', 'DI CARLO Alessia']
mens_labels = [
    'BOUNABI Akram', 'SAAD Youcef Abdelaziz',  # way far up
    'ZEA Gibran', 'ROMERO Eliecer', 'AMER Mohamed', 'AKINYOSOYE Oluwafolayemi',
    "D'ARMIENTO Francesco", 'XU Haojun', 'TSUBO Hayato']


# Create 2 scatterplots in data_analysis/pr_scatterplot_sabre_2025.png
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
make_scatter(ax1, womens, 550, 'Womens Sabre Senior 2024/2025', 'pagerank_rank', 'PageRank', womens_labels, 0)
make_scatter(ax2, mens, 1000, 'Mens Sabre Senior 2024/2025', 'pagerank_rank', 'PageRank', mens_labels, 0)
fig.suptitle('PageRank Rank vs FIE Rank — Sabre Senior 2024/2025',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('data_analysis/pr_scatterplot_sabre_2025.png', dpi=300, bbox_inches='tight')


# Create 2 scatterplots in data_analysis/ts_scatterplot_sabre_2025.png (trueskill vs FIE)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
make_scatter(ax1, womens, 550, 'Womens Sabre Senior 2024/2025', 'ts_rank_3sigma', 'TrueSkill', womens_labels, 0)
make_scatter(ax2, mens, 1000, 'Mens Sabre Senior 2024/2025', 'ts_rank_3sigma', 'TrueSkill', mens_labels, 0)
fig.suptitle('TrueSkill Rank vs FIE Rank — Sabre Senior 2024/2025',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('data_analysis/ts_scatterplot_sabre_2025.png', dpi=300, bbox_inches='tight')


# Country-coded Scatterplot PageRank
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
make_scatter(ax1, womens, 550, 'Womens Sabre Senior 2024/2025', 'pagerank_rank', 'PageRank', womens_labels, 1)
make_scatter(ax2, mens, 1000, 'Mens Sabre Senior 2024/2025', 'pagerank_rank', 'PageRank', mens_labels, 1)
fig.suptitle('PageRank vs FIE Rankings by Region — Sabre Senior 2024/2025',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('data_analysis/pr_scatter_sabre_2025_regional.png', dpi=300, bbox_inches='tight')


# Country-coded Scatterplot TrueSkill
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
make_scatter(ax1, womens, 550, 'Womens Sabre Senior 2024/2025', 'ts_rank_3sigma', 'TrueSkill', womens_labels, 1)
make_scatter(ax2, mens, 1000, 'Mens Sabre Senior 2024/2025', 'ts_rank_3sigma', 'TrueSkill', mens_labels, 1)
fig.suptitle('TrueSkill vs FIE Rankings by Region — Sabre Senior 2024/2025',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('data_analysis/ts_scatter_sabre_2025_regional.png', dpi=300, bbox_inches='tight')


# Sigma-coded Scatterplot TrueSkill
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
make_scatter(ax1, womens, 550, 'Womens Sabre Senior 2024/2025', 'ts_rank_3sigma', 'TrueSkill', womens_labels, 2)
make_scatter(ax2, mens, 1000, 'Mens Sabre Senior 2024/2025', 'ts_rank_3sigma', 'TrueSkill', mens_labels, 2)
fig.suptitle('TrueSkill vs FIE Rankings by Sigma — Sabre Senior 2024/2025',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('data_analysis/ts_scatter_sabre_2025_sigma.png', dpi=300, bbox_inches='tight')


# Outlier Details ----------------------------------------------------------------------------------
SEASON     = 2025
FIE_SEASON = '2024/2025'
WEAPON     = 'Sabre'

output_lines = []   # what to store in outlier_bouts.txt
outliers = [        # only the ones underranked by FIE
    {'name': 'DI CARLO Alessia',   'gender': 'Womens', 'date': 'Jun_26_2026', 'div': 'all_womens_sabre'},
    {'name': 'KIKUCHI Kokona',     'gender': 'Womens', 'date': 'Jun_26_2026', 'div': 'all_womens_sabre'},
    {'name': 'WEI Jiayi',          'gender': 'Womens', 'date': 'Jun_26_2026', 'div': 'all_womens_sabre'},
    {'name': 'XU Haojun',          'gender': 'Mens',   'date': 'Jun_28_2026', 'div': 'all_mens_sabre'},
    {"name": "D'ARMIENTO Francesco",'gender': 'Mens',  'date': 'Jun_28_2026', 'div': 'all_mens_sabre'},
    {"name": "TSUBO Hayato",        'gender': 'Mens',  'date': 'Jun_28_2026', 'div': 'all_mens_sabre'},
    {"name": "VIGH Benedek",        'gender': 'Mens',  'date': 'Jun_28_2026', 'div': 'all_mens_sabre'},
]

for fencer_info in outliers:
    name   = fencer_info['name']
    gender = fencer_info['gender']
    date   = fencer_info['date']
    div    = fencer_info['div']
    
    # load division-specific data (cos we only need mens/womens sabre)
    path         = f'output/{date}/{div}'
    bout_df      = pd.read_csv(path + f'_bout_data_{date}.csv')
    tournament_df= pd.read_csv(path + f'_tournament_data_{date}.csv')
    fencer_bio_df= pd.read_csv(path + f'_fencer_bio_data_{date}.csv')
    
    # get fencer ID
    fencer_row = fencer_bio_df[fencer_bio_df['name'] == name]
    if fencer_row.empty: print(f"WARNING: {name} not found")
    fencer_id = fencer_row['id'].iloc[0]
    country = fencer_row['country'].iloc[0]
    
    # get PageRank and FIE ranks
    comp = comparison_df[
        (comparison_df['id']       == fencer_id) &
        (comparison_df['season']   == FIE_SEASON) &
        (comparison_df['weapon']   == WEAPON) &
        (comparison_df['gender']   == gender) &
        (comparison_df['category'] == 'Senior')
    ]
    fie_rank      = comp['fie_rank'].iloc[0]      if not comp.empty else 'N/A'
    pagerank_rank = comp['pagerank_rank'].iloc[0] if not comp.empty else 'N/A'
    rank_diff     = comp['rank_diff'].iloc[0]     if not comp.empty else 'N/A'
    
    # fencer_ID, opp_ID, fencer_age, opp_age, fencer_score, opp_score, winner_ID, fencer_curr_pts, opp_curr_pts, tournament_ID, pool_ID, upset, date, round, bout_type, season, category
    bouts = bout_df[
        (bout_df['season'] == SEASON) &
        (bout_df['category'] == 'Senior') &
        ((bout_df['fencer_ID'] == fencer_id) | (bout_df['opp_ID'] == fencer_id))
    ].copy()
    if len(bouts) == 0: print(f"WARNING: no bouts found for {name}")
    
    # standardize (std) curr fencer to always be on the left side
    bouts['is_winner'] = bouts['winner_ID'] == fencer_id
    bouts['opponent_ID'] = bouts.apply(     # fenced_id vs bouts['opponent_ID']
        lambda r: r['opp_ID'] if r['fencer_ID'] == fencer_id else r['fencer_ID'], axis=1)
    bouts['fencer_score_std'] = bouts.apply(
        lambda r: r['fencer_score'] if r['fencer_ID'] == fencer_id else r['opp_score'], axis=1)
    bouts['opp_score_std'] = bouts.apply(
        lambda r: r['opp_score'] if r['fencer_ID'] == fencer_id else r['fencer_score'], axis=1)
    
    # get opponent FIE & PageRank ranks
    opp_fie = fie_df[
        (fie_df['season']   == FIE_SEASON) &
        (fie_df['weapon']   == WEAPON) &
        (fie_df['gender']   == gender) &
        (fie_df['category'] == 'Senior')
    ][['id', 'fie_rank', 'name']].rename(columns={
        'id': 'opponent_ID', 'fie_rank': 'opp_fie_rank', 'name': 'opp_name'
    })
    bouts = bouts.merge(opp_fie, on='opponent_ID', how='left')
    opp_pr = pagerank_df[
        (pagerank_df['season'].astype(str) == str(SEASON)) &
        (pagerank_df['weapon']   == WEAPON) &
        (pagerank_df['gender']   == gender) &
        (pagerank_df['category'] == 'Senior')
    ][['id', 'pagerank_rank']].rename(columns={
        'id': 'opponent_ID', 'pagerank_rank': 'opp_pagerank_rank'})
    bouts = bouts.merge(opp_pr, on='opponent_ID', how='left')
    
    # fill in opponent name from bio if not in FIE rankings
    bouts['opp_name'] = bouts.apply(
        lambda r: r['opp_name'] if pd.notna(r['opp_name'])  # opp_name already filled
        else fencer_bio_df[fencer_bio_df['id'] == r['opponent_ID']]['name'].values[0]   # unranked fencer
             if len(fencer_bio_df[fencer_bio_df['id'] == r['opponent_ID']]) > 0
        else f"NO NAME: {str(int(r['opponent_ID']))}",    # just show the ID
        axis=1
    )
    
    # print header
    output_lines.append(f"\n{'='*70}")
    output_lines.append(f"  {name} ({country}) - {fencer_id}")
    output_lines.append(f"  FIE Rank: {fie_rank}  |  PageRank: {pagerank_rank}  |  Diff: {rank_diff}")
    output_lines.append(f"  Total Tournaments: {bouts['tournament_ID'].nunique()}")
    wins = bouts['is_winner'].sum()
    output_lines.append(f"  {len(bouts)} Total Bouts:\t{wins}W, {len(bouts)-wins}L ({wins/len(bouts):.1%})")
    pool_bouts_total = len(bouts[bouts['bout_type'] == 'pool'])
    de_bouts_total   = len(bouts[bouts['bout_type'] == 'DE'])
    pool_wins_total  = bouts[bouts['bout_type'] == 'pool']['is_winner'].sum()
    de_wins_total    = bouts[bouts['bout_type'] == 'DE']['is_winner'].sum()
    output_lines.append(f"  {pool_bouts_total} Pool Bouts:\t{pool_wins_total}W, {pool_bouts_total - pool_wins_total}L")
    output_lines.append(f"  {de_bouts_total} DE Bouts:\t\t{de_wins_total}W, {de_bouts_total - de_wins_total}L")
    output_lines.append(f"{'='*70}")
    
    # print bouts grouped by tournament
    for tourn_id, tourn_bouts in bouts.groupby('tournament_ID'):
        tourn_row  = tournament_df[tournament_df['unique_ID'] == tourn_id]
        tourn_name = tourn_row['name'].iloc[0]    if len(tourn_row) > 0 else tourn_id
        tourn_loc  = tourn_row['country'].iloc[0] if len(tourn_row) > 0 else ''
        
        # sort pools first then DE by round
        round_order = {None: 0, 'A256': 1, 'A128A64': 2, 'A64': 3,
                       'A32': 4, 'A16': 5, 'A8': 6, 'A4': 7, 'A2': 7}
        tourn_bouts = tourn_bouts.copy()
        tourn_bouts['sort_key'] = tourn_bouts['round'].map(round_order).fillna(0)
        tourn_bouts = tourn_bouts.sort_values('sort_key')
        
        pool_wins  = tourn_bouts[tourn_bouts['bout_type'] == 'pool']['is_winner'].sum()
        pool_total = len(tourn_bouts[tourn_bouts['bout_type'] == 'pool'])
        de_wins    = tourn_bouts[tourn_bouts['bout_type'] == 'DE']['is_winner'].sum()
        de_total   = len(tourn_bouts[tourn_bouts['bout_type'] == 'DE'])
        
        output_lines.append(f"\n  [{tourn_name} — {tourn_loc}]")
        output_lines.append(f"  Pools: {pool_wins}/{pool_total}  |  DE: {de_wins}/{de_total}")
        output_lines.append(f"  {'Type':<5} {'Round':<6} {'Result':<7} {'Score':<6} {'Opponent':<28} {'Opp FIE Rank':<13} {'Opp PR Rank'}")
        output_lines.append(f"  {'-'*75}")
        
        for _, bout in tourn_bouts.iterrows():
            bout_type = bout['bout_type']
            round_    = bout['round'] if pd.notna(bout['round']) else 'pool'
            result    = 'WIN' if bout['is_winner'] else 'LOSS'
            score     = f"{int(bout['fencer_score_std'])}-{int(bout['opp_score_std'])}"
            opp_name  = bout['opp_name'][:28]
            opp_fie   = f"#{int(bout['opp_fie_rank'])}" if pd.notna(bout['opp_fie_rank']) else 'unranked'
            opp_pr   = f"#{int(bout['opp_pagerank_rank'])}" if pd.notna(bout['opp_pagerank_rank']) else 'unranked'
            
            output_lines.append(f"  {bout_type:<5} {round_:<6} {result:<7} {score:<6} {opp_name:<28} {opp_fie:<13} {opp_pr}")

with open('data_analysis/outlier_bouts.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))
print("\nSaved outlier_bouts.txt")


# OPPONENT QUALITY ANALYSIS (underranked fencers only) -------------------------------------------
UPSET_THRESHOLD = 20

def build_opponent_quality_table(bout_df, fie_lookup, rank_min, rank_max, season):
    valid_fencers = fie_lookup[     # id, fie_rank
        (fie_lookup['fie_rank'] >= rank_min) &
        (fie_lookup['fie_rank'] <= rank_max)
    ]['id'].tolist()
    valid_ids = set(valid_fencers)  # id
    
    totals = {fid: {    # dict - for each valid fencer, track these variables
        'opp_rank_sum_pool': 0, 'n_bouts_pool': 0,
        'opp_rank_sum_de':   0, 'n_bouts_de':   0,
        'n_better_opp_pool': 0, 'n_upsets_pool': 0,
        'n_better_opp_de':   0, 'n_upsets_de':   0,
        'own_rank': None
    } for fid in valid_ids}
    
    season_bouts = bout_df[
        (bout_df['season']   == season) &
        (bout_df['category'] == 'Senior')
    ]
    
    fie_rank_dict = dict(zip(fie_lookup['id'], fie_lookup['fie_rank']))
    
    for bout in season_bouts.itertuples():
        f_id, o_id   = bout.fencer_ID, bout.opp_ID
        winner_id    = bout.winner_ID
        is_pool      = bout.bout_type == 'pool'
        
        for this_id, opp_id in [(f_id, o_id), (o_id, f_id)]:
            if this_id not in valid_ids:
                continue
            
            max_rank = fie_lookup['fie_rank'].max()
            unranked_value = max_rank + 50      # default for unranked opponents
            opp_rank = fie_rank_dict.get(opp_id, unranked_value)
            
            own_rank = fie_rank_dict.get(this_id)
            totals[this_id]['own_rank'] = own_rank
            won = (winner_id == this_id)
            
            if is_pool:
                totals[this_id]['opp_rank_sum_pool'] += opp_rank
                totals[this_id]['n_bouts_pool'] += 1
                if own_rank is not None and (own_rank - opp_rank) >= UPSET_THRESHOLD:
                    totals[this_id]['n_better_opp_pool'] += 1
                    if won:
                        totals[this_id]['n_upsets_pool'] += 1
            else:  # DE
                totals[this_id]['opp_rank_sum_de'] += opp_rank
                totals[this_id]['n_bouts_de'] += 1
                if own_rank is not None and (own_rank - opp_rank) >= UPSET_THRESHOLD:
                    totals[this_id]['n_better_opp_de'] += 1
                    if won:
                        totals[this_id]['n_upsets_de'] += 1
    
    records = []
    for fid, t in totals.items():
        if t['n_bouts_pool'] == 0 and t['n_bouts_de'] == 0:
            continue
        records.append({
            'fencer_id':          fid,
            'own_fie_rank':       t['own_rank'],
            'n_bouts_pool':       t['n_bouts_pool'],
            'avg_opp_rank_pool':  t['opp_rank_sum_pool'] / t['n_bouts_pool'] if t['n_bouts_pool'] > 0 else None,
            'n_bouts_de':         t['n_bouts_de'],
            'avg_opp_rank_de':    t['opp_rank_sum_de'] / t['n_bouts_de'] if t['n_bouts_de'] > 0 else None,
            'n_bouts_comb':       t['n_bouts_de']+t['n_bouts_pool'],
            'avg_opp_rank_comb':  (t['opp_rank_sum_de']+t['opp_rank_sum_pool']) / (t['n_bouts_de']+t['n_bouts_pool']) if t['n_bouts_de']+t['n_bouts_pool'] > 0 else None,
            'n_better_opp_pool':  t['n_better_opp_pool'],
            'n_upsets_pool':      t['n_upsets_pool'],
            'upset_rate_pool':    t['n_upsets_pool'] / t['n_better_opp_pool'] if t['n_better_opp_pool'] > 0 else None,
            'n_better_opp_de':    t['n_better_opp_de'],
            'n_upsets_de':        t['n_upsets_de'],
            'upset_rate_de':      t['n_upsets_de'] / t['n_better_opp_de'] if t['n_better_opp_de'] > 0 else None,
            'n_better_opp_comb':  t['n_better_opp_de']+t['n_better_opp_pool'],
            'n_upsets_comb':      t['n_upsets_pool']+t['n_upsets_de'],
            'upset_rate_comb':    (t['n_upsets_de']+t['n_upsets_pool']) / (t['n_better_opp_de']+t['n_better_opp_pool']) if (t['n_better_opp_de']+t['n_better_opp_pool']) > 0 else None,
        })
    
    return pd.DataFrame(records)

def run_opponent_quality_section(gender, weapon, rank_min, rank_max, date, div, outlier_names, log_lines):
    path    = f'output/{date}/{div}'
    bout_df = pd.read_csv(path + f'_bout_data_{date}.csv')
    fencer_bio_df = pd.read_csv(path + f'_fencer_bio_data_{date}.csv')
    
    fie_lookup = fie_df[
        (fie_df['season']   == FIE_SEASON) &
        (fie_df['weapon']   == weapon) &
        (fie_df['gender']   == gender) &
        (fie_df['category'] == 'Senior')
    ][['id', 'fie_rank']]
    
    pop_df = build_opponent_quality_table(bout_df, fie_lookup, rank_min, rank_max, SEASON)
    
    log_lines.append(f"\n{'='*85}")
    log_lines.append(f"  OPPONENT QUALITY — {gender} {weapon} FIE ranks {rank_min}-{rank_max}")
    log_lines.append(f"  Population size: {len(pop_df)} fencers")
    log_lines.append(f"{'='*85}")
    log_lines.append(f"  POOLS    — avg opp rank: {pop_df['avg_opp_rank_pool'].mean():.1f}\t|  "
                      f"avg upset rate: {pop_df['upset_rate_pool'].mean():.1%}\t|  "
                      f"avg upsets: {pop_df['n_upsets_pool'].mean():.2f}")
    log_lines.append(f"  DE       — avg opp rank: {pop_df['avg_opp_rank_de'].mean():.1f}\t|  "
                      f"avg upset rate: {pop_df['upset_rate_de'].mean():.1%}\t|  "
                      f"avg upsets: {pop_df['n_upsets_de'].mean():.2f}")
    log_lines.append(f"  Combined — avg opp rank: {pop_df['avg_opp_rank_comb'].mean():.1f}\t|  "
                      f"avg upset rate: {pop_df['upset_rate_comb'].mean():.1%}\t|  "
                      f"avg upsets: {pop_df['n_upsets_comb'].mean():.2f}")
    
    log_lines.append(f"\n--------- OUTLIERS (underranked by FIE) ---------")
    for name in outlier_names:
        row = fencer_bio_df[fencer_bio_df['name'] == name]
        if row.empty:
            print(f"{name}: not found")
            continue
        fid = row['id'].iloc[0]
        fencer_row = pop_df[pop_df['fencer_id'] == fid]
        if fencer_row.empty:
            print(f"{name}: not in population")
            continue
        r = fencer_row.iloc[0]
        pr_row = pagerank_df[
            (pagerank_df['id']       == fid) &
            (pagerank_df['season'].astype(str) == str(SEASON)) &
            (pagerank_df['weapon']   == weapon) &
            (pagerank_df['gender']   == gender) &
            (pagerank_df['category'] == 'Senior')
        ]
        pr_rank = int(pr_row['pagerank_rank'].iloc[0]) if not pr_row.empty else None
        pr_rank_str = f"{pr_rank}" if pr_rank is not None else 'N/A'

        log_lines.append(f"\n  {name} (FIE rank #{int(r['own_fie_rank'])}, PR Rank #{pr_rank_str})")
        upset_rate_pool_str = f"{r['upset_rate_pool']:.1%}" if pd.notna(r['upset_rate_pool']) else 'N/A'
        upset_rate_de_str   = f"{r['upset_rate_de']:.1%}"   if pd.notna(r['upset_rate_de'])   else 'N/A'
        upset_rate_comb_str = f"{r['upset_rate_comb']:.1%}" if pd.notna(r['upset_rate_comb']) else 'N/A'
        log_lines.append(f"    POOLS: avg_opp_rank={r['avg_opp_rank_pool']:.1f}\t"
                        f"n_bouts={r['n_bouts_pool']}\t"
                        f"vs_better={r['n_better_opp_pool']}\t"
                        f"upsets={r['n_upsets_pool']}\t"
                        f"upset_rate={upset_rate_pool_str}")
        log_lines.append(f"    DE:    avg_opp_rank={r['avg_opp_rank_de']:.1f}\t"
                        f"n_bouts={r['n_bouts_de']}\t"
                        f"vs_better={r['n_better_opp_de']}\t"
                        f"upsets={r['n_upsets_de']}\t"
                        f"upset_rate={upset_rate_de_str}")
        log_lines.append(f"    COMB:  avg_opp_rank={r['avg_opp_rank_comb']:.1f}\t"
                        f"n_bouts={r['n_bouts_comb']}\t"
                        f"vs_better={r['n_better_opp_comb']}\t"
                        f"upsets={r['n_upsets_comb']}\t"
                        f"upset_rate={upset_rate_comb_str}")

opponent_log = []
run_opponent_quality_section(
    'Womens', 'Sabre', 64, 128, 'Jun_26_2026', 'all_womens_sabre',
    ['DI CARLO Alessia', 'KIKUCHI Kokona', 'WEI Jiayi'], opponent_log
)
run_opponent_quality_section(
    'Mens', 'Sabre', 128, 256, 'Jun_28_2026', 'all_mens_sabre',
    ["D'ARMIENTO Francesco", 'XU Haojun', 'TSUBO Hayato', 'VIGH Benedek'], opponent_log
)

with open('data_analysis/opponent_quality_analysis.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(opponent_log))
print("Saved opponent_quality_analysis.txt")
