from pydantic import BaseModel

class GenerateCodePayload(BaseModel):
    file_path : str
    prompt : str
    userId : str

class metaDataFilePayloads(BaseModel):
    file_path : str

class ChartDataPayload(BaseModel):
    sessionId : str
    x : dict[str,str]
    y : dict[str,str]
