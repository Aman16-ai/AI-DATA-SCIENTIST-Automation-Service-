from pydantic import BaseModel

class GenerateCodePayload(BaseModel):
    file_path : str
    prompt : str