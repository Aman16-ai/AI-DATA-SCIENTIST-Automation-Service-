from .llm import *
from .executeCode import runCode
def performFeatureEngineering(file,query):
    df = pandas.read_csv(file)
    code = generateCode(query,df)
    clearCode = clearGenerateCode(code)
    print(clearCode)
    writeCodeInFile(clearCode)
    runCode("python input.py")

