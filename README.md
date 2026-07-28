## Project Overview - Hannah Liu

Analysis of international fencing rankings using PageRank and TrueSkill ranking models.

## My Contributions

### Data Processing
- `add_category_to_bouts.py` — adds age category column to bout data
- `combine_fie_data.py` — combines FIE rankings across divisions and seasons into a single file
- `merge_rankings.py` — combines FIE, PageRank, and TrueSkill rankings into a single file containing only fencers ranked by all three systems

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

### Output
- `data_analysis/` — all CSVs, tables, and figures referenced in the paper

## Data
Raw bout data was collected using the fie-fencing-dataset scraper 
(amichaelsen, 2021): https://github.com/amichaelsen/fie-fencing-dataset 
with a few minor edits. Raw bout-level data is available upon request for 
academic research purposes.  
Processed data files are available in data_analysis/.

## Requirements
```bash
pip install pandas networkx trueskill scipy matplotlib
