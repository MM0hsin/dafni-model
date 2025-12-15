import pandas as pd

df = pd.read_csv("used_cars_10M_2025.csv")

uk_names = ["UK", "United Kingdom", "U.K."]
df_uk = df[df["country"].isin(uk_names)]

df_uk = df_uk.drop(columns=["country"])

df_uk.to_csv("clean_cars_data_uk.csv", index=False)

