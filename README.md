## Project Overview - Hannah Liu

Analysis of international fencing rankings using PageRank and TrueSkill ranking models.

## My Contributions

### Data Processing
- add_category_to_bouts.py — adds age category column to bout data
- combine_fie_data.py — combines FIE rankings across divisions

### Ranking Models  
- pagerank.py — builds PageRank rankings per season/division
- trueskill_model.py — builds TrueSkill rankings per season/division

### Analysis
- analysis.py — analyze differences between FIE, PageRank, and TrueSkill rankings
- spearman.py — Spearman correlation between ranking models
- sensitivity.py — PageRank parameter sensitivity testing
- prediction.py / ts_prediction.py — predictive validity testing for PageRank and TrueSkill

### Output
- data_analysis/ — all CSVs and figures referenced in the paper

## Data
Raw bout data was collected using the fie-fencing-dataset scraper 
(amichaelsen, 2021): https://github.com/amichaelsen/fie-fencing-dataset 
with a few minor edits. Raw bout-level data is available upon request for 
academic research purposes.  
Processed data files are available in data_analysis/.

## Requirements
pip install pandas networkx trueskill scipy matplotlib
