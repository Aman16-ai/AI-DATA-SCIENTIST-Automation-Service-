import pandas as pd
import numpy as np
import json

class MetaData:

    def __init__(self,file_path:str):
        self.file_path = file_path
        try:
            self.df = pd.read_excel(file_path)
            # print(self.df.head())
        except Exception as e:
            print(e)

    def attribute_types(self,df: pd.DataFrame) -> dict[str, type]:
        """
        Function to return the types of attributes in each column of a DataFrame.

        Args:
        df (pd.DataFrame): Input DataFrame.

        Returns:
        Dict[str, type]: Dictionary where keys are column names and values are attribute types.
        """
        attribute_dict = {}
        for col in df.columns:
            attribute_dict[col] = str(df[col].dtype)
        return attribute_dict

    def data(self):
        head_data = self.df.head().to_json(orient='records')
        head_data_json = json.loads(head_data)

        shape = self.df.shape

        attributesType = self.attribute_types(self.df)

        totalNAValues = self.df.isna().sum()
        totalNAValues_json = json.loads(totalNAValues.to_json(orient='records'))
        
        return {'head':head_data_json,'shape':shape,'attribute types':json.dumps(attributesType),"totalNAvalues":totalNAValues_json}