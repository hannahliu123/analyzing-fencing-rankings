import pandas as pd
import statsmodels.api as sm

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


# run regression
def run_regression(data, target_column, model_label):
    X_dummies = pd.get_dummies(
        data[["region"]], dtype=int, prefix="", prefix_sep=""
    )
    X = X_dummies.drop(columns=["Africa/Middle East"])
    X = sm.add_constant(X)

    y = data[target_column]

    model = sm.OLS(y, X).fit()
    log.append(f"\n" + "-" * 35 + f" {model_label} " + "-" * 35)
    log.append(model.summary().as_text())
    p_values = model.pvalues
    log.append(f"\nExact {model_label} p-values with high precision:")
    for variable, p_val in p_values.items():    # 20 decimal places
        log.append(f"{variable}: {p_val:.20f}")

run_regression(     # pr mens
    mens_df, target_column="pr_rank_diff_common", model_label="MENS PageRank"
)
run_regression(     # ts mens
    mens_df, target_column="ts_rank_diff_common", model_label="MENS TrueSkill"
)
run_regression(     # pr womens
    womens_df, target_column="pr_rank_diff_common", model_label="WOMENS PageRank"
)
run_regression(     # ts womens
    womens_df, target_column="ts_rank_diff_common", model_label="WOMENS TrueSkill"
)

# find averages per region
men_region_averages = (
    mens_df
    .groupby("region")[["pr_rank_diff_common", "ts_rank_diff_common"]]
    .mean()
)
women_region_averages = (
    womens_df
    .groupby("region")[["pr_rank_diff_common", "ts_rank_diff_common"]]
    .mean()
)
log.append("\n~~~~~~~~~~~~~~~~~~~~~~~~~ Men's Tabulation Averages ~~~~~~~~~~~~~~~~~~~~~~~~~")
log.append(men_region_averages.to_string())
log.append("\n~~~~~~~~~~~~~~~~~~~~~~~~ Women's Tabulation Averages ~~~~~~~~~~~~~~~~~~~~~~~~")
log.append(women_region_averages.to_string())

# save data
with open('data_analysis/regression.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(log))
print("\nSaved regression.txt")