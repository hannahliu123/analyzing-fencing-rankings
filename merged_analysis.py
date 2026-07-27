from scipy.stats import spearmanr
import pandas as pd
import matplotlib.pyplot as plt

merged_df = pd.read_csv('data_analysis/merged_rankings.csv')

region_colors = {
    'Europe':            '#4575b4',
    'Asia':              '#d73027',
    'Americas':          '#1a9850',
    'Africa/Middle East':'#fdae61',
    'Other':             '#bababa',
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
    if use_region==1:   # based on region
        df = df.copy()
        df['region'] = df['country'].apply(get_region)
        for region, group in df.groupby('region'):
            ax.scatter(
                group['fie_rank_common'], group[rank],
                alpha=0.5, s=20, color=region_colors[region], label=region
            )
    else:
        ax.scatter(
            df['fie_rank_common'], df[rank],
            alpha=0.5, s=20, color='steelblue'
        )

    ax.plot([1, lim-lim/150], [1, lim-lim/150],   # diagonal line
            color='red', linestyle='--', linewidth=1, alpha=0.7, label='Perfect agreement')
    
    for _, row in df.iterrows():
        name = row['name']
        if name in label_these:
            last_name = name.split()[0]
            if last_name == "DI": last_name = "DI CARLO"    # heh shhh
            if last_name == "KIKUCHI" and rank_name == "TrueSkill": continue    # shhh
            ax.annotate(
                last_name,
                xy=(row['fie_rank_common'], row[rank]),
                xytext=(row['fie_rank_common'] + lim/110, row[rank] - lim/140),
                fontsize=7, alpha=0.8, fontweight='bold'
            )
    
    ax.set_xlim(-lim/100, lim)
    ax.set_ylim(-lim/100, lim)
    ax.set_xlabel('Official FIE Rank', fontsize=11)
    ax.set_ylabel(f'{rank_name} Rank', fontsize=11)
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.legend(loc='lower right', fontsize=9)
    
    ax.grid(alpha=0.2)
    print(f"Finished plotting {len(df)} fencers with {rank_name}")


# Create scatterplot from merged_rankings.csv -----------------------------------------
sabre_2025 = merged_df[
    (merged_df['weapon']   == 'Sabre') &
    (merged_df['category'] == 'Senior') &
    (merged_df['fie_season']   == '2024/2025')
].copy()
womens = sabre_2025[sabre_2025['gender'] == 'Womens'].copy()
mens = sabre_2025[sabre_2025['gender'] == 'Mens'].copy()


# Decide who to do case studies on
pr_or_ts = 'pagerank_rank_common'     # pagerank_rank_common or ts_rank_3sigma_common
diff = 'pr_rank_diff_common'      # pr_rank_diff_common or ts_rank_diff_common
abs = 'abs_pr_rank_diff_common'     # abs_pr_rank_diff_common or abs_ts_rank_diff_common
womens_notable = womens[
    ((womens[pr_or_ts] <= 100) | (womens['fie_rank_common'] <= 100)) & (womens[abs] >= 50)
].sort_values(abs, ascending=False)
mens_notable = mens[
    ((mens[pr_or_ts] <= 150) | (mens['fie_rank_common'] <= 150)) & (mens[abs] >= 50)
].sort_values(abs, ascending=False)
print("\n=== WOMENS SABRE SENIOR 2024/2025 — Top 64 Notable Divergences ===")
print(womens_notable[['name', pr_or_ts, 'fie_rank_common', diff, abs]].to_string(index=False))
print("\n=== MENS SABRE SENIOR 2024/2025 — Top 64 Notable Divergences ===")
print(mens_notable[['name', pr_or_ts, 'fie_rank_common', diff, abs]].to_string(index=False))

womens_labels = [
    'BOUAJINA Aicha', 'REZGUI Yesmine', 'ELDOKSH Renad ',   # way far up
    'KEHLI Zohra Nora', 'BENADOUDA Chaima ', 'HAFEZ Nada', 'HEGAZY Alanoud', 'CARVALHO Isabela',
    'WEI Jiayi', 'KIKUCHI Kokona', 'DI CARLO Alessia']
mens_labels = [
    'BOUNABI Akram', 'SAAD Youcef Abdelaziz',  # way far up
    'ZEA Gibran', 'ROMERO Eliecer', 'AMER Mohamed', 'AKINYOSOYE Oluwafolayemi',
    "D'ARMIENTO Francesco", 'XU Haojun', 'TSUBO Hayato']


# Country-coded Scatterplot PageRank
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
make_scatter(ax1, womens, 450, 'Womens Sabre Senior 2024/2025', 'pagerank_rank_common', 'PageRank', womens_labels, 1)
make_scatter(ax2, mens, 650, 'Mens Sabre Senior 2024/2025', 'pagerank_rank_common', 'PageRank', mens_labels, 1)
fig.suptitle('PageRank vs FIE Rankings by Region — Sabre Senior 2024/2025',
             fontsize=18, fontweight='bold', y=1.01)
fig.text(0.5, 0.95, "Note: Smaller rank values indicate stronger skill. Ex. Rank #1 = Best", 
         fontsize=13, color='gray', ha='center', va='center')
plt.savefig('data_analysis/merged_pr_scatter_sabre_2025_regional.png', dpi=300, bbox_inches='tight')

# Country-coded Scatterplot TrueSkill
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
make_scatter(ax1, womens, 450, 'Womens Sabre Senior 2024/2025', 'ts_rank_3sigma_common', 'TrueSkill', womens_labels, 1)
make_scatter(ax2, mens, 650, 'Mens Sabre Senior 2024/2025', 'ts_rank_3sigma_common', 'TrueSkill', mens_labels, 1)
fig.suptitle('TrueSkill vs FIE Rankings by Region — Sabre Senior 2024/2025',
             fontsize=18, fontweight='bold', y=1.01)
fig.text(0.5, 0.95, "Note: Smaller rank values indicate stronger skill. Ex. Rank #1 = Best", 
         fontsize=13, color='gray', ha='center', va='center')
plt.savefig('data_analysis/merged_ts_scatter_sabre_2025_regional.png', dpi=300, bbox_inches='tight')


# ties
# rank_cols = {
#     "FIE": "fie_rank_common",
#     "PageRank": "pagerank_rank_common",
#     "TrueSkill": "ts_rank_3sigma_common"
# }

# rows = []

# for system, col in rank_cols.items():
#     counts = merged_df[col].value_counts()

#     tied_rank_values = counts[counts > 1]
#     fencers_in_ties = merged_df[col].isin(tied_rank_values.index).sum()

#     rows.append({
#         "system": system,
#         "total_fencers": len(merged_df),
#         "unique_rank_values": merged_df[col].nunique(),
#         "tied_rank_values": len(tied_rank_values),
#         "fencers_in_tied_ranks": fencers_in_ties,
#         "pct_fencers_in_tied_ranks": 100 * fencers_in_ties / len(merged_df),
#         "largest_tie_size": tied_rank_values.max() if len(tied_rank_values) > 0 else 1
#     })

# tie_summary = pd.DataFrame(rows)
# print(tie_summary)