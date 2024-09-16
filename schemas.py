from pydantic import BaseModel

class GenerateCodePayload(BaseModel):
    file_path : str
    prompt : str
    userId : int

class metaDataFilePayloads(BaseModel):
    file_path : str

class ChartDataPayload(BaseModel):
    file_path : str
    x : str
    y : str