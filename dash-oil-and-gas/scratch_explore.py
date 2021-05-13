import pandas as pd
import sqlite3 as sql

import sqlalchemy as sqlalchemy

df_explore = pd.read_csv(r"C:\git\bls\data\cu\cu.data.0.Current", sep="\t")
df_series = pd.read_csv(r"C:\git\bls\data\cu\cu.series", sep="\t")
current_period = df_explore.query("year == 2021 & period =='M04'")



sqlite = sqlalchemy.pool.manage(sql, poolclass=sqlalchemy.pool.StaticPool )
conn = sqlite.connect(':memory:')


df_explore.to_sql('current_data',conn)
df_series.to_sql('series',conn)

test =  pd.read_sql("""
                        SELECT * FROM current_data
                                    LEFT JOIN items on current_data.series_id = 
                    """


                    , conn)
