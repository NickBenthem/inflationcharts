import timeit
starttime = timeit.default_timer()

import pandas as pd
import sqlite3 as sql
import sqlalchemy as sqlalchemy

# https://www.bls.gov/cpi/data.htm
def read_bls_df(filepath):
    df = pd.read_csv(filepath,sep="\t")
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    df.columns = df.columns.str.strip()

    return df

df_explore = read_bls_df(r"C:\git\bls\data\cu\cu.data.0.Current") # Adding the nrows to go faster. This is big and Pycharm doesn't like it.
df_series = read_bls_df(r"C:\git\bls\data\cu\cu.series")
df_items = read_bls_df(r"C:\git\bls\data\cu\cu.item")


sqlite = sqlalchemy.pool.manage(sql, poolclass=sqlalchemy.pool.StaticPool )
conn = sqlite.connect(':memory:')


df_explore.to_sql('current_data', conn)
df_series.to_sql('series', conn)
df_items.to_sql('items', conn)

test =  pd.read_sql("""
                        SELECT current_data.value, items.item_name, series.begin_year || '-' || substr(series.begin_period,2,4) as date
                         FROM current_data
                                    LEFT JOIN series on series.series_id = current_data.series_id
                                    LEFT JOIN items on series.item_code = items.item_code
                    """
                    , conn)

test.to_csv(r"C:\git\bls\dash-inflation\bls_joined_data.csv",index=False)

print(f"runtime is {timeit.default_timer() - starttime}")