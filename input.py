import pandas as pd
import numpy as np

df = pd.read_csv('test_df.csv')


df = df[df['salary'] > 65000]
print(df)
df = df[df['salary'] > 65000]
print(df)
print(df.isnull().sum())
from sklearn.model_selection import train_test_split

def train_test_split_salary(df):
    X = df.drop(['salary'], axis=1)
    y = df['salary']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

X_train, X_test, y_train, y_test = train_test_split_salary(df)

print(X_train.head())
print(X_test.head())
print(y_train.head())
print(y_test.head())
from sklearn.model_selection import train_test_split

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df[['age', 'city', 'salary']], df['name'], test_size=0.25, random_state=42)

# Standardize the training and testing data
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Print the standardized data
print(X_train)
print(X_test)