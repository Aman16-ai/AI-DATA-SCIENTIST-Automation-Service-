from .llm import *
from .executeCode import runCode
import os
def performFeatureEngineering(file,query,userId):
    df = pandas.read_excel(file)
    code = generateCode(query,df,file)
    clearCode = clearGenerateCode(code)
    print(clearCode)
    file_path = os.path.join(UPLOAD_DIR,f"{userId}_inputfile.py")
    # if(not os.path.exists(file_path)):
    #     writeConfigCode(file_path,file)

    writeConfigCode(file_path,file)
    writeCodeInFile(clearCode,file_path)
    output = runCode("python "+file_path)
    print(type(output))
    return output

