import pandas as pd

df_explore = pd.read_csv(r"C:\git\bls\data\cu\cu.data.0.Current", sep="\t")
df_items = pd.read_csv(r"C:\git\bls\data\cu\cu.item", sep="\t")
current_period = df_explore.query("year == 2021 & period =='M04'")



