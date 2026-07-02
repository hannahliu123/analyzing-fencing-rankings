
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import pandas as pd

comparison_df = pd.read_csv('data_analysis/all_pagerank_fie_comparisons.csv')

# Create data_analysis/fie_spearman_comparisions.csv -----------------------------------------------
spearman_records = []
for (weapon, gender, category, season), group in comparison_df.groupby(
    ['weapon', 'gender', 'category', 'season']):
    
    if len(group) < 10:     # for early seasons with very few fencers
        continue
    
    rho, pvalue = spearmanr(group['pagerank_rank'], group['fie_rank'])
    if pd.isna(rho): continue
    # season, weapon, gender, category, rho, pvalue, n_fencers
    if season == "2013/2014": continue   # edge case, just ignore it :P
    spearman_records.append({
        'season':    season,
        'weapon':    weapon,
        'gender':    gender,
        'category':  category,
        'rho':       round(rho, 4),
        'pvalue':    pvalue,
        'n_fencers': len(group)
    })

spearman_df = pd.DataFrame(spearman_records)
spearman_df = spearman_df.sort_values(
    ['weapon', 'gender', 'category', 'season']
)
spearman_df.to_csv('data_analysis/fie_spearman_comparisons.csv', index=False)
print(f"Saved {len(spearman_df)} Spearman results")

# Interpret Spearman Correlation Results (mean, min, max summary statistics)
print("=== AVERAGE RHO BY CATEGORY ===")
category_summary = spearman_df.groupby('category')['rho'].agg(
    mean='mean', min='min', max='max', count='count'
).round(4)
print(category_summary)

print("\n=== AVERAGE RHO BY CATEGORY (excluding 2020/2021) ===")
no_covid = spearman_df[spearman_df['season'] != '2020/2021']
category_summary_no_covid = no_covid.groupby('category')['rho'].agg(
    mean='mean', min='min', max='max', count='count'
).round(4)
print(category_summary_no_covid)

print("\n=== NUMBER OF FENCERS (NODES) PER SEASON BY CATEGORY ===")
fencers_per_category = spearman_df.groupby('category')['n_fencers'].agg(
    mean='mean', min='min', max='max'
).round(2)
print(fencers_per_category)

# Interpret Spearman Correlation Results (line graph by season)
senior_df = spearman_df[spearman_df['category'] == 'Senior'].copy()
senior_df['season_year'] = senior_df['season'].apply(
    lambda s: int(s.split('/')[1])  # 2020/2021 -> 2021 because it fits better on a graph
)
senior_df['division'] = senior_df['weapon'] + ' ' + senior_df['gender']
divisions = senior_df['division'].unique()
colors = {
    'Foil Womens':  '#E63946',
    'Epee Womens':  '#457B9D',
    'Sabre Womens': '#2A9D8F',
    'Foil Mens':    '#E9C46A',
    'Epee Mens':    '#F4A261',
    'Sabre Mens':   '#6A4C93',
}

fig, ax = plt.subplots(figsize=(12, 6)) # width, height
for division, group in senior_df.groupby('division'):
    group = group.sort_values('season_year')  # make sure seasons go left to right
    ax.plot(
        group['season_year'],    # x
        group['rho'],            # y
        marker='o',              # draw a dot at each data point
        markersize=5,            # dot size
        linewidth=2,             # line thickness
        color=colors.get(division),
        label=division           # label for the legend
    )

ax.axhline(y=0, color='black', linewidth=0.8, alpha=0.3)
ax.axvline(x=2021, color='gray', linestyle='--', alpha=0.6, linewidth=1.5)  # COVID
ax.text(2021.1, 0.35, 'COVID-19', fontsize=9, color='gray')
ax.set_xlabel('Season (end year)', fontsize=12)         # x axis
ax.set_ylabel('Spearman Correlation (ρ)', fontsize=12)  # y axis
ax.set_title('PageRank vs FIE Senior Rankings — Spearman Correlation by Season',
             fontsize=13, fontweight='bold')
ax.set_ylim(0.3, 1.0)   # y axis range
ax.set_xticks(sorted(senior_df['season_year'].unique()))
plt.xticks(rotation=45, ha='right')     # rotate x labels so they don't overlap
ax.legend(loc='lower right', fontsize=10)   # show legend
ax.grid(axis='y', alpha=0.3)    # gridlines
plt.tight_layout()      # prevents labels from being cut off
plt.savefig('data_analysis/spearman_by_season.png', dpi=300, bbox_inches='tight')
