
import numpy as np
import pandas as pd
import sklearn
df = pd.read_csv("test_df.csv")

df = df[df['salary']>65000]
print(df)
# Get the dataframe
df = pd.read_csv('test_df.csv')

# Perform the query
df_filtered = df[df['age'] > 38]

# Print the updated dataframe
print(df_filtered)