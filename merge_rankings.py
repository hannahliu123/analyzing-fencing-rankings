# Merge FIE, PR, and TS rankings for fencers that appear in all 3 models

import pandas as pd
import os

fie_df = pd.read_csv('data_analysis/all_fie_rankings.csv')
pagerank_df = pd.read_csv('data_analysis/all_pagerank_rankings.csv')
trueskill_df = pd.read_csv('data_analysis/all_trueskill_rankings.csv')

fie_df = fie_df.rename(columns={"season": "fie_season"})
common_keys = ["id", "fie_season", "category", "weapon", "gender"]

fie_df = fie_df[common_keys + ["fie_score", "fie_rank"]].copy()
pagerank_df = pagerank_df[common_keys + ["pagerank_score", "pagerank_rank"]].copy()
trueskill_df = trueskill_df[common_keys + ["ts_score_3sigma", "ts_rank_3sigma"]].copy()

merged = (
    fie_df
    .merge(pagerank_df, on=common_keys, how="inner")    # inner-join = keep only fencers present in all 3 systems
    .merge(trueskill_df, on=common_keys, how="inner")
)

merged["fie_rank_common"] = (
    merged.groupby(["fie_season", "category", "weapon", "gender"])["fie_score"]
    .rank(method="min", ascending=False)
)
merged["pagerank_rank_common"] = (
    merged.groupby(["fie_season", "category", "weapon", "gender"])["pagerank_score"]
    .rank(method="min", ascending=False)
)
merged["ts_rank_3sigma_common"] = (
    merged.groupby(["fie_season", "category", "weapon", "gender"])["ts_score_3sigma"]
    .rank(method="min", ascending=False)
)

merged["pr_rank_diff_common"] = merged["fie_rank_common"] - merged["pagerank_rank_common"]
merged["ts_rank_diff_common"] = merged["fie_rank_common"] - merged["ts_rank_3sigma_common"]

path = 'data_analysis/merged_rankings.csv'
merged.to_csv(path, index=False)
print(f"Created {path} with {len(merged)} records")
