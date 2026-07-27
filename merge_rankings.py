# Merge FIE, PR, and TS rankings for fencers that appear in all 3 models

import pandas as pd

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
        'NEW ZEALAND', 'AUSTRALIA', 'BRUNEI DARUSSALAM', "MACAO, CHINA",
        'SYRIAN ARAB REPUBLIC'
    ]
    americas = [
        'UNITED STATES', 'UNITED STATES OF AMERICA', 'USA',
        'CANADA', 'BRAZIL', 'MEXICO', 'ARGENTINA', 'CUBA',
        'VENEZUELA', 'COLOMBIA', 'PERU', 'CHILE', 'ECUADOR',
        'PANAMA', 'DOMINICAN REPUBLIC', 'TRINIDAD AND TOBAGO',
        'PUERTO RICO', 'URUGUAY', 'PARAGUAY', 'BOLIVIA',
        'COSTA RICA', 'GUATEMALA', 'HONDURAS', 'EL SALVADOR',
        'NICARAGUA', 'JAMAICA', 'BARBADOS', 'HAITI', 'GUYANA',
        'SURINAME', 'BELIZE', 'ARUBA', 'VIRGIN ISLANDS', 'BERMUDA',
        'ANTIGUA AND BARBUDA', 'DOMINICA'
    ]
    africa_me = [
        'EGYPT', 'ALGERIA', 'TUNISIA', 'MOROCCO', 'LIBYA', 'SUDAN',
        'SENEGAL', 'SOUTH AFRICA', 'NIGERIA', 'GHANA', 'CAMEROON',
        'IVORY COAST', "COTE D'IVOIRE", 'MADAGASCAR', 'KENYA',
        'ETHIOPIA', 'TANZANIA', 'UGANDA', 'ZIMBABWE', 'ZAMBIA',
        'MOZAMBIQUE', 'ANGOLA', 'NAMIBIA', 'BOTSWANA', 'TOGO',
        'BENIN', 'MALI', 'BURKINA FASO', 'NIGER', 'CHAD',
        'DEMOCRATIC REPUBLIC OF CONGO', 'REPUBLIC OF CONGO',
        'RWANDA', 'BURUNDI', 'SOMALIA', 'ERITREA', 'DJIBOUTI',
        'MAURITIUS', 'SEYCHELLES', 'CAPE VERDE', 'GAMBIA',
        'GUINEA', 'GUINEA-BISSAU', 'SIERRA LEONE', 'LIBERIA',
        'SAUDI ARABIA', 'UAE', 'UNITED ARAB EMIRATES', 'QATAR',
        'KUWAIT', 'BAHRAIN', 'IRAQ', 'JORDAN', 'LEBANON',
        'SYRIA', 'ISRAEL', 'PALESTINE', 'OMAN', 'YEMEN',
        'CAPE VERDE '
    ]
    
    if country in europe:   return 'Europe'
    if country in asia:     return 'Asia'
    if country in americas: return 'Americas'
    if country in africa_me: return 'Africa/Middle East'
    print(f"country {country} resulted in an invalid region")
    return 'Other'

fie_df = pd.read_csv('data_analysis/all_fie_rankings.csv')
pagerank_df = pd.read_csv('data_analysis/all_pagerank_rankings.csv')
trueskill_df = pd.read_csv('data_analysis/all_trueskill_rankings.csv')

fie_df = fie_df.rename(columns={"season": "fie_season"})
common_keys = ["id", "fie_season", "category", "weapon", "gender"]

fie_df = fie_df[common_keys + ["name", "country", "fie_score", "fie_rank"]].copy()
fie_df = fie_df.rename(columns={"fie_rank": "fie_rank_common"})
fie_df["region"] = fie_df["country"].apply(get_region)
pagerank_df = pagerank_df[common_keys + ["pagerank_score", "pagerank_rank"]].copy()
trueskill_df = trueskill_df[common_keys + ["ts_score_3sigma", "ts_rank_3sigma"]].copy()

merged = (
    fie_df
    .merge(pagerank_df, on=common_keys, how="inner")    # inner-join = keep only fencers present in all 3 systems
    .merge(trueskill_df, on=common_keys, how="inner")
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
merged["abs_pr_rank_diff_common"] = merged["pr_rank_diff_common"].abs()
merged["abs_ts_rank_diff_common"] = merged["ts_rank_diff_common"].abs()

path = 'data_analysis/merged_rankings.csv'
merged.to_csv(path, index=False)
print(f"Created {path} with {len(merged)} records")
