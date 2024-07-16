import numpy as np 
import pandas as pd 
df = pd.read_excel("http://localhost:5000/uploads/excel-files/1715310467058crop_production.xlsx")
def func():
    global df
    return df.isnull().sum()
func()