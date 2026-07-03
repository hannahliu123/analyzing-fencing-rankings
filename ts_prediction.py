# does season X TrueSkill better predict season X+1 bout outcomes than FIE? and which of 4 ts models

import pandas as pd

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

def run_prediction_test(bout_df, trueskill_df, fie_df, weapon, gender, category,
                        season_x, season_x1, log_lines):
    
    fie_season_x  = f"{season_x-1}/{season_x}"      # season to train on (FIE format)
    
    # get season X rankings for both systems
    fie_x = fie_df[
        (fie_df['season']   == fie_season_x) &
        (fie_df['weapon']   == weapon) &
        (fie_df['gender']   == gender) &
        (fie_df['category'] == category)
    ][['id', 'fie_rank']].set_index('id')['fie_rank'].to_dict()
    
    ts_rank_dict = trueskill_df[
        (trueskill_df['season'].astype(str) == str(season_x)) &
        (trueskill_df['weapon'] == weapon) &
        (trueskill_df['gender'] == gender) &
        (trueskill_df['category'] == category)
    ][['id', 'ts_rank_3sigma', 'ts_rank_2sigma', 'ts_rank_1sigma', 'ts_rank_mu']].set_index('id')[
        ['ts_rank_mu', 'ts_rank_1sigma', 'ts_rank_2sigma', 'ts_rank_3sigma']
    ].apply(list, axis=1).to_dict()
    
    # get season X+1 bouts
    bouts_x1 = bout_df[
        (bout_df['season']   == season_x1) &    # season to test
        (bout_df['category'] == category)
    ]
    
    fie_correct = 0
    ts3_correct = 0
    ts2_correct = 0
    ts1_correct = 0
    ts0_correct = 0
    total = 0
    fie_de = 0
    ts3_de = 0
    ts2_de = 0
    ts1_de = 0
    ts0_de = 0
    de_total = 0
    
    for bout in bouts_x1.itertuples():
        f_id = bout.fencer_ID
        o_id = bout.opp_ID
        winner_id = bout.winner_ID
        
        f_fie = fie_x.get(f_id)
        o_fie = fie_x.get(o_id)
        tsf_data = ts_rank_dict.get(f_id)
        tso_data = ts_rank_dict.get(o_id)
        f_ts3 = tsf_data[3] if tsf_data is not None else None
        o_ts3 = tso_data[3] if tso_data is not None else None
        f_ts2 = tsf_data[2] if tsf_data is not None else None
        o_ts2 = tso_data[2] if tso_data is not None else None
        f_ts1 = tsf_data[1] if tsf_data is not None else None
        o_ts1 = tso_data[1] if tso_data is not None else None
        f_ts0 = tsf_data[0] if tsf_data is not None else None
        o_ts0 = tso_data[0] if tso_data is not None else None
        
        # both systems can make a prediction
        if (f_fie is not None and o_fie is not None and
            tsf_data is not None and tso_data is not None):
            total += 1
            fie_winner = f_id if f_fie < o_fie else o_id
            if fie_winner == winner_id:
                fie_correct += 1
            
            ts_winner = f_id if f_ts3 < o_ts3 else o_id
            if ts_winner == winner_id:
                ts3_correct += 1
            ts_winner = f_id if f_ts2 < o_ts2 else o_id
            if ts_winner == winner_id:
                ts2_correct += 1
            ts_winner = f_id if f_ts1 < o_ts1 else o_id
            if ts_winner == winner_id:
                ts1_correct += 1
            ts_winner = f_id if f_ts0 < o_ts0 else o_id
            if ts_winner == winner_id:
                ts0_correct += 1
            
            if bout.bout_type == "DE":
                de_total += 1
                if fie_winner == winner_id:
                    fie_de += 1
                
                ts_winner = f_id if f_ts3 < o_ts3 else o_id
                if ts_winner == winner_id:
                    ts3_de += 1
                ts_winner = f_id if f_ts2 < o_ts2 else o_id
                if ts_winner == winner_id:
                    ts2_de += 1
                ts_winner = f_id if f_ts1 < o_ts1 else o_id
                if ts_winner == winner_id:
                    ts1_de += 1
                ts_winner = f_id if f_ts0 < o_ts0 else o_id
                if ts_winner == winner_id:
                    ts0_de += 1
    
    fie_acc = fie_correct / total if total > 0 else None
    ts3_acc = ts3_correct / total if total > 0 else None
    ts2_acc = ts2_correct / total if total > 0 else None
    ts1_acc = ts1_correct / total if total > 0 else None
    ts0_acc = ts0_correct / total if total > 0 else None
    fie_de_acc = fie_de / de_total if de_total > 0 else None
    ts3_de_acc = ts3_de / de_total if de_total > 0 else None
    ts2_de_acc = ts2_de / de_total if de_total > 0 else None
    ts1_de_acc = ts1_de / de_total if de_total > 0 else None
    ts0_de_acc = ts0_de / de_total if de_total > 0 else None
    
    log_lines.append(
        f"  {season_x} → {season_x1}   "
        f"{fie_acc:.1%}  "
        f"{ts3_acc:.1%}  "
        f"{ts2_acc:.1%}  "
        f"{ts1_acc:.1%}  "
        f"{ts0_acc:.1%}  "
        # f"{(ts3_acc-fie_acc):+.1%}  "
        f"{fie_de_acc:.1%}   "
        f"{ts3_de_acc:.1%}   "
        f"{ts2_de_acc:.1%}   "
        f"{ts1_de_acc:.1%}   "
        f"{ts0_de_acc:.1%}   "
        # f"{(ts3_de_acc-fie_de_acc):+.1%}"
    )
    
    return {
        'season_x': season_x, 'season_x1': season_x1,  # train, test
        'fie_acc': fie_acc, 'ts3_acc': ts3_acc, 'ts2_acc': ts2_acc, 'ts1_acc': ts1_acc, 'ts0_acc': ts0_acc, 'total':  total,
        'fie_de_acc': fie_de_acc, 'ts3_de_acc': ts3_de_acc, 'ts2_de_acc': ts2_de_acc, 'ts1_de_acc': ts1_de_acc, 'ts0_de_acc': ts0_de_acc, 'de_total': de_total
    }


def run_all_prediction_tests(trueskill_df, fie_df, weapon, gender, category, date, div, log_lines):
    path    = f'output/{date}/{div}'
    bout_df = pd.read_csv(path + f'_bout_data_{date}.csv')
    
    log_lines.append(f"\n{'='*75}")
    log_lines.append(f"  PREDICTION TEST — {gender} {weapon} {category}")
    log_lines.append(f"  Predict season X+1 bout outcomes using season X rankings")
    log_lines.append(f"{'='*75}")
    log_lines.append(f"  {'Season Pair':<13} {'FIE':<6} {'TS3':6} {'TS2':<6} {'TS1':6} {'TS0':<6} {'DE FIE':<7} {'DE TS3':<7} {'DE TS2':<7} {'DE TS1':<7} {'DE TS0':<7}")
    log_lines.append(f"  {'-'*70}")
    
    results = []
    for sx, sx1 in season_pairs:    # for all seasons we want to test
        r = run_prediction_test(
            bout_df, trueskill_df, fie_df, weapon, gender, category, sx, sx1, log_lines
        )
        results.append(r)
    
    # summary
    results_df = pd.DataFrame(results).dropna(subset=['fie_acc', 'ts3_acc', 'ts2_acc', 'ts1_acc', 'ts0_acc', 'fie_de_acc', 'ts3_de_acc', 'ts2_de_acc', 'ts1_de_acc', 'ts0_de_acc'])
    log_lines.append(f"\n  Average FIE accuracy:     {results_df['fie_acc'].mean():.1%}")
    log_lines.append(f"  Average TS3 accuracy:     {results_df['ts3_acc'].mean():.1%}")
    log_lines.append(f"  Average TS2 accuracy:     {results_df['ts2_acc'].mean():.1%}")
    log_lines.append(f"  Average TS1 accuracy:     {results_df['ts1_acc'].mean():.1%}")
    log_lines.append(f"  Average TS0 accuracy:     {results_df['ts0_acc'].mean():.1%}")
    # diff = results_df['pr_acc'].mean() - results_df['fie_acc'].mean()
    # log_lines.append(f"  Difference (PR - FIE):    {diff:+.1%}")
    log_lines.append(f"  Average FIE DE accuracy:  {results_df['fie_de_acc'].mean():.1%}")
    log_lines.append(f"  Average TS3 DE accuracy:  {results_df['ts3_de_acc'].mean():.1%}")
    log_lines.append(f"  Average TS2 DE accuracy:  {results_df['ts2_de_acc'].mean():.1%}")
    log_lines.append(f"  Average TS1 DE accuracy:  {results_df['ts1_de_acc'].mean():.1%}")
    log_lines.append(f"  Average TS0 DE accuracy:  {results_df['ts0_de_acc'].mean():.1%}")
    # diff2 = results_df['pr_de_acc'].mean() - results_df['fie_de_acc'].mean()
    # log_lines.append(f"  DE Difference (PR - FIE): {diff2:+.1%}")
    
    return results_df

# Run predications for all divisions (Senior category)
pred_log  = []
all_results = []

for weapon, gender, date, div in divisions:
    results_df = run_all_prediction_tests(
        trueskill_df, fie_df, weapon, gender, 'Senior', date, div, pred_log
    )
    results_df['weapon'] = weapon
    results_df['gender'] = gender
    all_results.append(results_df)

# overall summary across all divisions
combined = pd.concat(all_results, ignore_index=True).dropna(subset=['fie_acc', 'ts3_acc', 'ts2_acc', 'ts1_acc', 'ts0_acc', 'fie_de_acc', 'ts3_de_acc', 'ts2_de_acc', 'ts1_de_acc', 'ts0_de_acc'])

pred_log.append(f"\n\n{'='*75}")
pred_log.append(f"  OVERALL SUMMARY — All Divisions Senior")
pred_log.append(f"{'='*75}")
pred_log.append(f"  Average FIE accuracy:    {combined['fie_acc'].mean():.1%}")
pred_log.append(f"  Average TS3 accuracy:    {combined['ts3_acc'].mean():.1%}")
pred_log.append(f"  Average TS2 accuracy:    {combined['ts2_acc'].mean():.1%}")
pred_log.append(f"  Average TS1 accuracy:    {combined['ts1_acc'].mean():.1%}")
pred_log.append(f"  Average TS0 accuracy:    {combined['ts0_acc'].mean():.1%}")
# pred_log.append(f"  Difference (PR - FIE):   {combined['ts_acc'].mean() - combined['fie_acc'].mean():+.1%}")
pred_log.append(f"  Average FIE DE accuracy: {combined['fie_de_acc'].mean():.1%}")
pred_log.append(f"  Average TS3 DE accuracy: {combined['ts3_de_acc'].mean():.1%}")
pred_log.append(f"  Average TS2 DE accuracy: {combined['ts2_de_acc'].mean():.1%}")
pred_log.append(f"  Average TS1 DE accuracy: {combined['ts1_de_acc'].mean():.1%}")
pred_log.append(f"  Average TS0 DE accuracy: {combined['ts0_de_acc'].mean():.1%}")
# pred_log.append(f"  Difference (PR - FIE):   {combined['pr_de_acc'].mean() - combined['fie_de_acc'].mean():+.1%}")
pred_log.append(f"  Total bouts evaluated:    {combined['total'].sum()}")
pred_log.append(f"  Total DE bouts evaluated: {combined['de_total'].sum()}")

pred_log.append(f"\n  --- By Division ---")
for (weapon, gender), group in combined.groupby(['weapon', 'gender']):
    pred_log.append(
        f"  {weapon} {gender}: "
        f"FIE={group['fie_acc'].mean():.1%}  "
        f"TS3={group['ts3_acc'].mean():.1%}  "
        f"TS2={group['ts2_acc'].mean():.1%}  "
        f"TS1={group['ts1_acc'].mean():.1%}  "
        f"TS0={group['ts0_acc'].mean():.1%}  "
        # f"diff={group['pr_acc'].mean() - group['fie_acc'].mean():+.1%}   "
        f"DEFIE={group['fie_de_acc'].mean():.1%}  "
        f"DETS3={group['ts3_de_acc'].mean():.1%}  "
        f"DETS2={group['ts2_de_acc'].mean():.1%}  "
        f"DETS1={group['ts1_de_acc'].mean():.1%}  "
        f"DETS0={group['ts0_de_acc'].mean():.1%}  "
        # f"DEdiff={group['pr_de_acc'].mean() - group['fie_de_acc'].mean():+.1%}"
    )

with open('data_analysis/ts_prediction_test.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(pred_log))
print("Saved prediction_test.txt")
