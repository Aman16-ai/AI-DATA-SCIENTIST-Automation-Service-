
import numpy as np
import pandas as pd
import sklearn
df = pd.read_excel("http://localhost:5000/uploads/excel-files/1715515031076crop_production.xlsx")

df = df.dropna()
print(df)