## Project Overview - Hannah Liu

Analysis of international fencing rankings using PageRank and TrueSkill ranking models.

## Scripts

### Data Processing
- `add_category_to_bouts.py` — adds age category column to bout data
- `combine_fie_data.py` — combines FIE rankings across divisions and seasons into a single file
- `merge_rankings.py` — combines FIE, PageRank, and TrueSkill rankings into a single file `merged_rankings.csv` containing only fencers ranked by all three systems

### Ranking Models  
- `pagerank.py` — builds PageRank rankings per season/division
- `trueskill_model.py` — builds TrueSkill rankings per season/division

### Data Analysis
- `analysis.py` — original script analyzing differences between FIE, PageRank, and TrueSkill rankings
- `merged_analysis.py` — updated script analyzing differences between FIE, PageRank, and TrueSkill rankings using merged dataset
- `spearman.py` — original script computing Spearman correlations between ranking models
- `merged_spearman.py` — updated script computing Spearman correlation between ranking models using merged dataset
- `sensitivity.py` — tests how PageRank rankings change under different pool weights and damping factors
- `prediction.py` / `ts_prediction.py` — evaluates how well PageRank and TrueSkill predict next-season bout outcomes
- `anova_tukey_region_analysis.py` — tests whether regional rank differences are statistically significant using one-way ANOVA and Tukey HSD

## Output
The `data_analysis/` folder contains all processed datasets, summary tables, figures, and analysis outputs used in the paper. The most important files include:

### Datasets
- `merged_rankings.csv` — merged FIE, PageRank, and TrueSkill rankings for fencers who appear in all three systems
- `merged_spearman_comparisions.csv` — Spearman correlation results computed from the merged dataset

### Regional analysis
- `merged_pr_scatter_sabre_2025_region.png` — PageRank vs. FIE scatterplot for Senior Sabre (2024/2025), colored by region
- `merged_ts_scatter_sabre_2025_region.png` — TrueSkill vs. FIE scatterplot for Senior Sabre (2024/2025), colored by region
- `merged_pr_spearman_by_season.png` — PageRank vs. FIE Spearman correlations by season
- `merged_ts_spearman_by_season.png` — TrueSkill vs. FIE Spearman correlations by season
- `anova_tukey_results.txt` — ANOVA and Tukey HSD output for regional rank differences

### Underranked-fencer analysis
- `opponent_quality_analysis.txt` — summary of opponent-quality metrics for baseline rank tiers and specific underranked fencers
- `outlier_bouts.txt` — bout-level data used to for specific underranked fencer case studies

### Predictive validity
- `prediction_test.txt` — PageRank next-season prediction results
- `ts_prediction_test.txt` — TrueSkill next-season prediction results

Additional intermediate CSVs, figures, and scratch files are also stored in this folder.

## Data
Raw bout data was collected using the fie-fencing-dataset scraper 
(amichaelsen, 2021): https://github.com/amichaelsen/fie-fencing-dataset 
with a few minor edits. Raw bout-level data is available upon request for 
academic research purposes.  
Processed data files are available in `data_analysis/`.

## Requirements
```bash
pip install pandas networkx trueskill scipy matplotlib statsmodels
```

## Questions
If you have any questions about this project, feel free to reach out to me through email.
