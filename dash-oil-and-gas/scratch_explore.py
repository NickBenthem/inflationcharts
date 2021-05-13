import timeit
starttime = timeit.default_timer()

import pandas as pd
import sqlite3 as sql
import sqlalchemy as sqlalchemy
# https://www.bls.gov/cpi/data.htm
df_explore = pd.read_csv(r"C:\git\bls\data\cu\cu.data.0.Current", sep="\t") # Adding the nrows to go faster. This is big and Pycharm doesn't like it.
df_series = pd.read_csv(r"C:\git\bls\data\cu\cu.series", sep="\t")

df_obj = df_series.select_dtypes(['object'])
df_explore_obj = df_explore.select_dtypes(['object'])
# https://stackoverflow.com/questions/40950310/strip-trim-all-strings-of-a-dataframe
df_series[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
df_explore[df_explore_obj.columns] = df_explore_obj.apply(lambda x: x.str.strip())

# https://stackoverflow.com/questions/21606987/how-can-i-strip-the-whitespace-from-pandas-dataframe-headers
df_series.columns = df_series.columns.str.strip()
df_explore.columns = df_explore.columns.str.strip()

# current_period = df_explore.query("year == 2021 & period =='M04'")

sqlite = sqlalchemy.pool.manage(sql, poolclass=sqlalchemy.pool.StaticPool )
conn = sqlite.connect(':memory:')


df_explore.to_sql('current_data',conn)
df_series.to_sql('series',conn)

test =  pd.read_sql("""
                        SELECT * FROM current_data
                                    LEFT JOIN series on series.series_id = current_data.series_id
                    """
                    , conn)

print(f"runtime is {timeit.default_timer() - starttime}")