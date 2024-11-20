
import numpy as np
import pandas as pd
import sklearn
df = pd.read_excel("http://localhost:5000/uploads/excel-files/1715515031076crop_production.xlsx")

from sklearn.model_selection import train_test_split

df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
print(df_train)
print(df_test)
