# does season X PageRank better predict season X+1 bout outcomes than FIE?

import pandas as pd

pagerank_df = pd.read_csv('data_analysis/all_pagerank_rankings.csv')
trueskill_df = pd.read_csv('data_analysis/all_trueskill_rankings.csv')
fie_df = pd.read_csv('data_analysis/all_fie_rankings.csv')

divisions = [
    ('Foil',  'Womens', 'Jun_25_2026', 'all_womens_foil'),
    ('Epee',  'Womens', 'Jun_27_2026', 'all_womens_epee'),
    ('Sabre', 'Womens', 'Jun_26_2026', 'all_womens_sabre'),
    ('Sabre', 'Mens',   'Jun_28_2026', 'all_mens_sabre'),
    ('Epee',  'Mens',   'Jun_29_2026', 'all_mens_epee'),
    ('Foil',  'Mens',   'Jun_30_2026', 'all_mens_foil'),
]

# seasons i want to analyze
season_pairs = [(2022, 2023), (2023, 2024), (2024, 2025)]

def run_prediction_test(bout_df, pagerank_df, trueskill_df, fie_df, weapon, gender, category,
                        season_x, season_x1, log_lines):

    restriction = 2000000   # restricted to fencers ranked in the top __
    margin = 0      # don't consider if the fencers are ranked within __ places of eachother
    
    fie_season_x  = f"{season_x-1}/{season_x}"      # season to train on (FIE format)
    
    # get season X rankings for both systems
    fie_x = fie_df[
        (fie_df['season']   == fie_season_x) &
        (fie_df['weapon']   == weapon) &
        (fie_df['gender']   == gender) &
        (fie_df['category'] == category)
    ][['id', 'fie_rank']].set_index('id')['fie_rank'].to_dict()
    
    pr_x = pagerank_df[
        (pagerank_df['season'].astype(str) == str(season_x)) &
        (pagerank_df['weapon']   == weapon) &
        (pagerank_df['gender']   == gender) &
        (pagerank_df['category'] == category)
    ][['id', 'pagerank_rank']].set_index('id')['pagerank_rank'].to_dict()

    ts_x = trueskill_df[
        (trueskill_df['season'].astype(str) == str(season_x)) &
        (trueskill_df['weapon'] == weapon) &
        (trueskill_df['gender'] == gender) &
        (trueskill_df['category'] == category)
    ][['id', 'ts_rank_3sigma']].set_index('id')['ts_rank_3sigma'].to_dict()
    
    # get season X+1 bouts
    bouts_x1 = bout_df[
        (bout_df['season']   == season_x1) &    # season to test
        (bout_df['category'] == category)
    ]
    
    fie_correct = 0
    pr_correct = 0
    ts_correct = 0
    fie_total = 0
    pr_total = 0
    ts_total = 0
    fie_de = 0
    pr_de = 0
    ts_de = 0
    fie_de_total = 0
    pr_de_total = 0
    ts_de_total = 0
    
    for bout in bouts_x1.itertuples():
        f_id = bout.fencer_ID
        o_id = bout.opp_ID
        winner_id = bout.winner_ID
        
        f_fie = fie_x.get(f_id)
        o_fie = fie_x.get(o_id)
        f_pr = pr_x.get(f_id)
        o_pr = pr_x.get(o_id)
        f_ts = ts_x.get(f_id)
        o_ts = ts_x.get(o_id)
        
        # fie prediction
        if (f_fie is not None or o_fie is not None):
            if (f_fie is None): f_fie = o_fie+1
            if (o_fie is None): o_fie = f_fie+1
            if (f_fie > restriction and o_fie > restriction): continue      # skip if not within top __
            if (abs(f_fie - o_fie) <= margin): continue      # skip if small margin
            fie_total += 1
            fie_winner = f_id if f_fie < o_fie else o_id
            if fie_winner == winner_id:
                fie_correct += 1
            if bout.bout_type == "DE":
                fie_de_total += 1
                if fie_winner == winner_id:
                    fie_de += 1

        # pr prediction
        if (f_pr is not None or o_pr is not None):
            if (f_pr is None): f_pr = o_pr+1
            if (o_pr is None): o_pr = f_pr+1
            if (f_pr > restriction and o_pr > restriction): continue      # skip if not within top __
            if (abs(f_pr - o_pr) <= margin): continue      # skip if small margin
            pr_total += 1
            pr_winner = f_id if f_pr < o_pr else o_id
            if pr_winner == winner_id:
                pr_correct += 1
            if bout.bout_type == "DE":
                pr_de_total += 1
                if pr_winner == winner_id:
                    pr_de += 1

        # ts prediction
        if (f_ts is not None or o_ts is not None):
            if (f_ts is None): f_ts = o_ts+1
            if (o_ts is None): o_ts = f_ts+1
            if (f_ts > restriction and o_ts > restriction): continue      # skip if not within top __
            if (abs(f_ts - o_ts) <= margin): continue      # skip if small margin
            ts_total += 1
            ts_winner = f_id if f_ts < o_ts else o_id
            if ts_winner == winner_id:
                ts_correct += 1
            if bout.bout_type == "DE":
                ts_de_total += 1
                if ts_winner == winner_id:
                    ts_de += 1
    
    fie_acc = fie_correct / fie_total if fie_total > 0 else None
    pr_acc = pr_correct / pr_total if pr_total > 0 else None
    ts_acc = ts_correct / ts_total if ts_total > 0 else None
    fie_de_acc = fie_de / fie_de_total if fie_de_total > 0 else None
    pr_de_acc = pr_de / pr_de_total if pr_de_total > 0 else None
    ts_de_acc = ts_de / ts_de_total if ts_de_total > 0 else None
    
    log_lines.append(
        f"  {season_x} → {season_x1}   "
        f"{fie_acc:.1%}  "
        f"{pr_acc:.1%}  "
        f"{(pr_acc-fie_acc):+.1%}  "
        f"{ts_acc:.1%}  "
        f"{(ts_acc-fie_acc):+.1%}  "
        f"{fie_de_acc:.1%}    "
        f"{pr_de_acc:.1%}    "
        f"{(pr_de_acc-fie_de_acc):+.1%}"
        f"{ts_de_acc:.1%}    "
        f"{(ts_de_acc-fie_de_acc):+.1%}"
    )
    
    return {
        'season_x': season_x, 'season_x1': season_x1,  # train, test
        'fie_correct': fie_correct, 'pr_correct': pr_correct, 'ts_correct': ts_correct,
        'fie_acc': fie_acc, 'pr_acc': pr_acc, 'ts_acc': ts_acc, 
        'fie_total': fie_total, 'pr_total': pr_total, 'ts_total': ts_total,
        'fie_de_acc': fie_de_acc, 'pr_de_acc': pr_de_acc, 'ts_de_acc': ts_de_acc,
        'fie_de_total': fie_de_total, 'pr_de_total': pr_de_total, 'ts_de_total': ts_de_total
    }


def run_all_prediction_tests(pagerank_df, fie_df, weapon, gender, category, date, div, log_lines):
    path    = f'output/{date}/{div}'
    bout_df = pd.read_csv(path + f'_bout_data_{date}.csv')
    
    log_lines.append(f"\n{'='*75}")
    log_lines.append(f"  PREDICTION TEST — {gender} {weapon} {category}")
    log_lines.append(f"  Predict season X+1 bout outcomes using season X rankings")
    log_lines.append(f"{'='*75}")
    log_lines.append(f"  {'Season Pair':<13} {'FIE':<6} {'PR':6} {'Diff':<6} {'TS':6} {'Diff':<6} {'DE FIE':<8} {'PR FIE':<8} {'DE Diff':<8} {'TS FIE':<8} {'DE Diff':<8}")
    log_lines.append(f"  {'-'*65}")
    
    results = []
    for sx, sx1 in season_pairs:    # for all seasons we want to test
        r = run_prediction_test(
            bout_df, pagerank_df, trueskill_df, fie_df, weapon, gender, category, sx, sx1, log_lines
        )
        results.append(r)
    
    # summary
    results_df = pd.DataFrame(results).dropna(subset=['fie_acc', 'pr_acc', 'ts_acc'])
    log_lines.append(f"\n  Average FIE accuracy:     {results_df['fie_acc'].mean():.1%}")
    log_lines.append(f"  Average PR accuracy:      {results_df['pr_acc'].mean():.1%}")
    diff = results_df['pr_acc'].mean() - results_df['fie_acc'].mean()
    log_lines.append(f"  Difference (PR - FIE):    {diff:+.1%}")
    log_lines.append(f"  Average TS accuracy:      {results_df['ts_acc'].mean():.1%}")
    diff = results_df['ts_acc'].mean() - results_df['fie_acc'].mean()
    log_lines.append(f"  Difference (TS - FIE):    {diff:+.1%}")
    log_lines.append(f"  Total FIE Correct:        {results_df['fie_correct'].sum()}")
    log_lines.append(f"  Total PR Correct:         {results_df['pr_correct'].sum()}")
    log_lines.append(f"  Total TS Correct:         {results_df['ts_correct'].sum()}")
    log_lines.append(f"  Total FIE Bouts:          {results_df['fie_total'].sum()}")
    log_lines.append(f"  Total PR Bouts:           {results_df['pr_total'].sum()}")
    log_lines.append(f"  Total TS Bouts:           {results_df['ts_total'].sum()}")
    log_lines.append(f"  Average FIE DE accuracy:  {results_df['fie_de_acc'].mean():.1%}")
    log_lines.append(f"  Average PR DE accuracy:   {results_df['pr_de_acc'].mean():.1%}")
    diff2 = results_df['pr_de_acc'].mean() - results_df['fie_de_acc'].mean()
    log_lines.append(f"  DE Difference (PR - FIE): {diff2:+.1%}")
    log_lines.append(f"  Average TS DE accuracy:   {results_df['ts_de_acc'].mean():.1%}")
    diff2 = results_df['ts_de_acc'].mean() - results_df['fie_de_acc'].mean()
    log_lines.append(f"  DE Difference (TS - FIE): {diff2:+.1%}")
    log_lines.append(f"  Total FIE DE Bouts:       {results_df['fie_de_total'].sum()}")
    # could add other totals if needed
    
    return results_df

# Run predications for all divisions (Senior category)
pred_log  = []
all_results = []

for weapon, gender, date, div in divisions:
    results_df = run_all_prediction_tests(
        pagerank_df, fie_df, weapon, gender, 'Senior', date, div, pred_log
    )
    results_df['weapon'] = weapon
    results_df['gender'] = gender
    all_results.append(results_df)

# overall summary across all divisions
combined = pd.concat(all_results, ignore_index=True).dropna(subset=['fie_acc', 'pr_acc'])

pred_log.append(f"\n\n{'='*75}")
pred_log.append(f"  OVERALL SUMMARY — All Divisions Senior")
pred_log.append(f"{'='*75}")
pred_log.append(f"  Average FIE accuracy:    {combined['fie_acc'].mean():.1%}")
pred_log.append(f"  Average PR accuracy:     {combined['pr_acc'].mean():.1%}")
pred_log.append(f"  Difference (PR - FIE):   {combined['pr_acc'].mean() - combined['fie_acc'].mean():+.1%}")
pred_log.append(f"  Average TS accuracy:     {combined['ts_acc'].mean():.1%}")
pred_log.append(f"  Difference (TS - FIE):   {combined['ts_acc'].mean() - combined['fie_acc'].mean():+.1%}")
pred_log.append(f"  Average FIE DE accuracy: {combined['fie_de_acc'].mean():.1%}")
pred_log.append(f"  Average PR DE accuracy:  {combined['pr_de_acc'].mean():.1%}")
pred_log.append(f"  Difference (PR - FIE):   {combined['pr_de_acc'].mean() - combined['fie_de_acc'].mean():+.1%}")
pred_log.append(f"  Average TS DE accuracy:  {combined['ts_de_acc'].mean():.1%}")
pred_log.append(f"  Difference (TS - FIE):   {combined['ts_de_acc'].mean() - combined['fie_de_acc'].mean():+.1%}")
pred_log.append(f"  Total FIE correct:       {combined['fie_correct'].sum()}")
pred_log.append(f"  Total PR correct:        {combined['pr_correct'].sum()}")
pred_log.append(f"  Total TS correct:        {combined['ts_correct'].sum()}")
pred_log.append(f"  Total FIE bouts evaluated:    {combined['fie_total'].sum()}")
pred_log.append(f"  Total PR bouts evaluated:     {combined['pr_total'].sum()}")
pred_log.append(f"  Total TS bouts evaluated:     {combined['ts_total'].sum()}")
pred_log.append(f"  Total FIE DE bouts evaluated: {combined['fie_de_total'].sum()}")
# could add other totals

pred_log.append(f"\n  --- By Division ---")
for (weapon, gender), group in combined.groupby(['weapon', 'gender']):
    pred_log.append(
        f"  {weapon} {gender}: "
        f"FIE={group['fie_acc'].mean():.1%}  "
        f"PR={group['pr_acc'].mean():.1%}  "
        f"diff={group['pr_acc'].mean() - group['fie_acc'].mean():+.1%}   "
        f"TS={group['ts_acc'].mean():.1%}  "
        f"diff={group['ts_acc'].mean() - group['fie_acc'].mean():+.1%}   "
        f"DEFIE={group['fie_de_acc'].mean():.1%}  "
        f"DEPR={group['pr_de_acc'].mean():.1%}  "
        f"DEdiff={group['pr_de_acc'].mean() - group['fie_de_acc'].mean():+.1%}"
        f"DETS={group['ts_de_acc'].mean():.1%}  "
        f"DEdiff={group['ts_de_acc'].mean() - group['fie_de_acc'].mean():+.1%}"
    )

with open('data_analysis/restricted_prediction_test.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(pred_log))
print("Saved restricted_prediction_test.txt")
