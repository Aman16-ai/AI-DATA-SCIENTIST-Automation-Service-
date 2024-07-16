import docker.errors
import pandas as pd
from llm_hf import llm_class
# from LLM.Feature_Engineering.llm_hf import llm_class
from dotenv import load_dotenv
import os
import re
import io
import numpy as np
import sklearn
import docker
from fastapi import HTTPException
import subprocess
load_dotenv()

# client = docker.from_env()
class feature_engineering:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.llm = llm_class(os.getenv("hf_email"), os.getenv("hf_passwd"))

    def perform_operation(self, query: str):
        prompt = f"""You are given a query along with a sample of data frame. Write a python function to perform that operation and return the updated dataframe.
        --------------------------------
        Strictly follow the given rules:
        1. The function should be named as 'func'.
        2. Dataframe is already read in the global scope just write the generated code in func.
        3. add a line in the start of func function that is global df.
        4. It will not accept any kind of arguments
        5. It should return the updated dataframe.
        6. Just return the python code nothing extra intro or explanation.
        7. Sklearn is already imported, Pandas is already imported as pd, Numpy as np.
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
        return gen_func
        # temp_file = io.StringIO()
        # try:
        #     temp_file.write(gen_func)
        #     temp_file.seek(0)  
        #     exec(temp_file.read(), globals())
        # except Exception as e:
        #     raise Exception(f"Error in running generated function: {e}")
            
        # self.df = func(self.df) # type: ignore

        # temp_file.close()
    
    def run(self,filepath,query):
        result = self.perform_operation(query=query)
        with open("inputfile.py",'w') as file:
            file.write(f'import numpy as np \nimport pandas as pd \ndf = pd.read_csv("{filepath}")')
            file.write("\n")
            file.write(result)
            file.write('\nfunc()')

        command = "python inputfile.py"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the process to finish and get the output
        stdout, stderr = process.communicate()

        # Check if there were any errors
        if process.returncode != 0:
            print("Error executing command:", stderr.decode())
        else:
            print("Command output:")
            print(stdout.decode())
        
    #     container_name = "code-execution-container"
    #     image_name = "python:3.9-slim"
    #     code_volume = {os.path.abspath("inputfile.py"): {"bind": "/code/inputfile.py", "mode": "rw"}}
    #     output_volume = {os.path.abspath("outputfile.txt"): {"bind": "/code/outputfile.txt", "mode": "rw"}}
    #     volumes = {**code_volume, **output_volume}

    # # Run the container
    #     try:
    #         client.containers.run(image_name, 
    #                            command="pip install numpy pandas",
    #                            detach=True)
    #         container = client.containers.run(image_name, 
    #                                         name=container_name,
    #                                         volumes=volumes,
    #                                         command="python /code/inputfile.py > /code/outputfile.txt",
    #                                         detach=True)
    #         container.wait()
    #     except docker.errors.ContainerError as e:
    #         print(e)
    #         raise HTTPException(status_code=500, detail="Error executing code in container")

    #     # Read the output file
    #     output = ""
    #     try:
    #         with open("outputfile.txt", "r") as file:
    #             output = file.read()
    #     except FileNotFoundError:
    #         raise HTTPException(status_code=500, detail="Output file not found")
        
    #     print(output)
       

df = pd.read_csv('./test_df.csv')
fe = feature_engineering(df)
query = "Filter the dataframe to include only rows where age is greater than 37 and after this print df using print()"
query2 = "check total na values"
fe.run("./test_df.csv",query)
# print(fe.df)

# def init(file_path,query):
#     df = pd.read_excel(file_path)
#     fe = feature_engineering(df)
#     fe.run(file_path,query)
