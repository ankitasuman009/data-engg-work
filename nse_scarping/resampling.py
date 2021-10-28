import pandas as pd
from pandas.core.arrays.sparse import dtype

df = pd.read_csv("one_year_data.csv")

# print(df["Date "].dtype)
df["Date "] = pd.to_datetime(df["Date "])
# print(df["Date "].dtype)
df = df.set_index(df["Date "])

df2 = df.resample('W').apply({'OPEN ': 'first',
          'HIGH ': 'max',
          'LOW ': 'min',
          'close ': 'last'})

print(df2.head())