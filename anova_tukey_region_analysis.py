# ANOVA analysis on merged dataset (alternative to regression)

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

df = pd.read_csv('data_analysis/merged_rankings.csv')
log = []

filtered_df = df[
    (df["fie_season"] == "2024/2025")
    & (df["weapon"] == "Sabre")
    & (df["category"] == "Senior")
].copy()
filtered_df = filtered_df[filtered_df["region"] != "Other"].copy()

mens_df = filtered_df[filtered_df["gender"] == "Mens"].copy()
womens_df = filtered_df[filtered_df["gender"] == "Womens"].copy()

def run_anova_and_tukey(data, target_col, title):
    log.append("\n" + "=" * 80)
    log.append(title)
    log.append("=" * 80)

    # means by region (and cnt and stdev)
    region_summary = (
        data.groupby("region")[target_col]
        .agg(count="count", mean="mean", std="std")
        .reset_index()
        .sort_values("region")
    )
    log.append("\nRegion summary:")
    log.append(region_summary.to_string(index=False))

    # ANOVA via OLS
    model = ols(f"{target_col} ~ C(region)", data=data).fit()   # target_col (rank diff) is response variable and region is categorical independent variable
    anova_table = sm.stats.anova_lm(model, typ=2)   # Type II Sum of Squares
    log.append("\nANOVA table:")
    log.append(anova_table.to_string())
    '''
    How to Interpret Output:
        - sum_sq (Sum of Squares): amount of variation in rank diff explained by region. 
            > higher number means region accounts for more variation in your data.
            > For Residuals, sum_sq is the variation your model could not explain (ideally low relative to your variables)
        - df (Degrees of Freedom): # groups-1
        - F (F-Statistic): ratio of the variance explained by region to the variance unexplained (Residuals).
            > close to 1 means region has little to no effect. The larger, the more likely region is truly impacting rank diff
        - PR(>F) (p-value): probability of obtaining an F-statistic this large (or larger) due to random chance alone
            > interpret like a normal p-value
    '''

    # Tukey HSD
    tukey = pairwise_tukeyhsd(
        endog=data[target_col],     # dependent variable (rank diff)
        groups=data["region"],      # independent variable
        alpha=0.05      # significance level
    )
    log.append("\nTukey HSD:")
    log.append(str(tukey))
    '''
    How to Interpret Output:
        - meandiff (Mean Difference): average value of group2 - average value of group1
        - p-adj (Adjusted p-value): probability that the meandiff happened by random chance.
            > this p-value has been "adjusted" upward to protect against accidental false positives from making multiple comparisons
            > interpret like a normal p-value
        - lower and upper: the lower and upper boundaries of the 95% confidence interval for the mean difference
            > If the range passes through 0, it means the true difference could be zero, so the result is not statistically significant
        - reject: whether to reject the null hypothesis
    '''

    return region_summary, anova_table, tukey

# compute all mens and womens analyses
men_pr_summary, men_pr_anova, men_pr_tukey = run_anova_and_tukey(
    mens_df, "pr_rank_diff_common", "Men's Sabre — PageRank vs FIE"
)
men_ts_summary, men_ts_anova, men_ts_tukey = run_anova_and_tukey(
    mens_df, "ts_rank_diff_common", "Men's Sabre — TrueSkill vs FIE"
)
women_pr_summary, women_pr_anova, women_pr_tukey = run_anova_and_tukey(
    womens_df, "pr_rank_diff_common", "Women's Sabre — PageRank vs FIE"
)
women_ts_summary, women_ts_anova, women_ts_tukey = run_anova_and_tukey(
    womens_df, "ts_rank_diff_common", "Women's Sabre — TrueSkill vs FIE"
)

# log everything
with open("data_analysis/anova_tukey_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(log))
print("Saved data_analysis/anova_tukey_results.txt")