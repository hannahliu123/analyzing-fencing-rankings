import pandas as pd
import statsmodels.api as sm

df = pd.read_csv('data_analysis/all_pagerank_trueskill_fie_comparisons.csv')

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


filtered_df = df[
    (df["season"] == "2024/2025")
    & (df["weapon"] == "Sabre")
    & (df["category"] == "Senior")
].copy()
filtered_df["region"] = filtered_df["country"].apply(get_region)

pr_y = filtered_df["rank_diff"]
ts_y = filtered_df["ts_rank_diff"]

# convert x-vars gender and region to dummy variables
X_all_dummies = pd.get_dummies(
    filtered_df[["gender", "region"]], dtype=int, prefix="", prefix_sep=""
)
X = X_all_dummies.drop(columns=["Mens", "Africa/Middle East"])  # baseline/reference groups
X = sm.add_constant(X)

print("\n" + "-" * 25 + " PR MODEL: Target = rank_diff " + "-" * 25)
pr_model = sm.OLS(pr_y, X).fit()
print(pr_model.summary())
pr_p_values = pr_model.pvalues
print("\nExact PR P-Values with high precision:")
for variable, p_val in pr_p_values.items():    # 20 decimal places
    print(f"{variable}: {p_val:.20f}")


print("\n" + "-" * 25 + " TS MODEL: Target = rank_diff " + "-" * 25)
ts_model = sm.OLS(ts_y, X).fit()
print(ts_model.summary())
ts_p_values = ts_model.pvalues
print("\nExact TS P-Values with high precision:")
for variable, p_val in ts_p_values.items():
    print(f"{variable}: {p_val:.20f}")
