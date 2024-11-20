import numpy as np
import pandas as pd
import json
class ChartData:

    def __init__(self,buffer):
        try:
            self.df = pd.read_excel(buffer)
            print(self.df.head())
        except Exception as e:
            print(e)
    
    def data(self,x,xType,y,yType):
        data = self.df.groupby(x)[y]

        if yType == 'count':
            return data.count()
        elif yType == 'max':
            return data.max()
        elif yType == 'min':
            return data.min()
        elif yType == 'mean':
            return data.mean()
        elif yType == 'median':
            return data.median()
        else:
            return data.sum()
