import numpy as np 
import pandas as pd 
df = pd.read_csv("./test_df.csv")
def func():
    global df
    df = df[df['age'] > 37]
    print(df)
func()