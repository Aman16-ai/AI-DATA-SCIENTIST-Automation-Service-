from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import pandas
import re
from settings import UPLOAD_DIR
from dotenv import load_dotenv
load_dotenv()
# 1. import all necessary modules of data science and machine learning accroding to the use
# 7. Sklearn is already imported, Pandas is already imported as pd, Numpy as np.
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY",'noi noi')

def clearGenerateCode(code):
    try:
            # gen_func = '\n'.join(gen_func.split('\n')[2:-1])
            cleanCode = ''
            pattern = r'```python\n(.*?)\n```'
            match = re.search(pattern, code, re.DOTALL)
            if match:
                cleanCode = match.group(1)
                return cleanCode
            else:
                raise ValueError("Generated function code not found.")
    except:
        pass
    
def generateCode(query,df,file):
    input_prompt = """You are professional machine learning engineer. You are given a query along with a sample of data frame. Write a python function to perform that operation and return the updated dataframe.
        --------------------------------
        Strictly follow the given rules:
        1. Dataframe is already import using pandas.
        3. Just write the generate code
        4. if need to update the df update the df also with new df
        5. print the ouput using print
        6. Just write the python code nothing extra intro or explanation.
        7. Sklearn is already imported, Pandas is already imported as pd, Numpy as np.
        Rules ENDS
        --------------------------------
        Query: {query}
        df columns: {cols}
        df sample rows: {rows}"""
    

    prompt = PromptTemplate.from_template(input_prompt)
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser

    code = chain.invoke({'file':file,
                         'query':query,
                         'cols':df.columns,
                         'rows':df.head(min(3,df.shape[0]))})

    return code



def writeCodeInFile(code,file_path):
    
    with open(file_path,'+a') as file:
        file.write("\n"+code)


from core.data_science_config_code import init
def writeConfigCode(file_path,dataFile):
     with open(file_path,"w") as file:
          file.write(init(dataFile))
# df = pandas.read_csv('test_df.csv')
# code = generateCode('give the name with highest salary',df)
# clearCode = clearGenerateCode(code)
# print(clearCode)
# writeCodeInFile(clearCode)

