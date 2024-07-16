import numpy as np
import pandas as pd
import json
class ChartData:

    def __init__(self,file_path):
        self.file_path = file_path
        try:
            self.df = pd.read_excel(file_path)
        except Exception as e:
            print(e)
    
    def data(self,x,y):
        x = self.df[x].to_json(orient='records')
        y = self.df[y].to_json(orient='records')
        print(x)
        return {"x":json.loads(x),"y":json.loads(y)}
