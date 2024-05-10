import pandas as pd
from llm_hf import llm_class
from dotenv import load_dotenv
import os
import re
import io
import numpy as np
import sklearn
load_dotenv()


class feature_engineering:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.llm = llm_class(os.getenv("hf_email"), os.getenv("hf_passwd"))

    def perform_operation(self, query: str):
        prompt = f"""You are given a query along with a sample of data frame. Write a python function to perform that operation and return the updated dataframe.
        --------------------------------
        Strictly follow the given rules:
        1. The function should be named as 'func'.
        2. It should take only one input that is dataframe.
        3. It should return the updated dataframe.
        4. Just return the python code nothing extra intro or explanation.
        5. Sklearn is already imported, Pandas is already imported as pd, Numpy as np.
        Rules ENDS
        --------------------------------
        Query: {query}
        df columns: {self.df.columns}
        df sample rows: {self.df.head(min(3,self.df.shape[0]))}"""
        
        gen_func = self.llm.ask(prompt=prompt)
        try:
            # gen_func = '\n'.join(gen_func.split('\n')[2:-1])
            pattern = r'```python\n(.*?)\n```'
            match = re.search(pattern, gen_func, re.DOTALL)
            if match:
                gen_func = match.group(1)
            else:
                raise ValueError("Generated function code not found.")
        except:
            pass
        
        print(gen_func)
        
        temp_file = io.StringIO()
        try:
            temp_file.write(gen_func)
            temp_file.seek(0)  
            exec(temp_file.read(), globals())
        except Exception as e:
            raise Exception(f"Error in running generated function: {e}")
            
        self.df = func(self.df) # type: ignore

        temp_file.close()

df = pd.read_csv('./test_df.csv')
fe = feature_engineering(df)
query = "Filter the dataframe to include only rows where age is greater than 30"
fe.perform_operation(query)
print(fe.df)
