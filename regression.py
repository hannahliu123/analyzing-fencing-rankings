import pandas as pd
import statsmodels.api as sm

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
    print(f"country {country} resulted in an invalid region")
    return 'Other'

df = pd.read_csv('data_analysis/all_pagerank_trueskill_fie_comparisons.csv')
log = []

filtered_df = df[
    (df["season"] == "2024/2025")
    & (df["weapon"] == "Sabre")
    & (df["category"] == "Senior")
].copy()
filtered_df["region"] = filtered_df["country"].apply(get_region)

mens_df = filtered_df[filtered_df["gender"] == "Mens"].copy()
womens_df = filtered_df[filtered_df["gender"] == "Womens"].copy()

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
    mens_df, target_column="rank_diff", model_label="MENS PageRank"
)
run_regression(     # ts mens
    mens_df, target_column="ts_rank_diff", model_label="MENS TrueSkill"
)
run_regression(     # pr womens
    womens_df, target_column="rank_diff", model_label="WOMENS PageRank"
)
run_regression(     # ts womens
    womens_df, target_column="ts_rank_diff", model_label="WOMENS TrueSkill"
)

with open('data_analysis/regression.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(log))
print("\nSaved regression.txt")
