from fastapi import FastAPI
from schemas import GenerateCodePayload
from metaData.main import MetaData
import json
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/fetchFileMetaData")
def fetchFileMetaData(paylaod: GenerateCodePayload):
    metaData = MetaData(paylaod.file_path)
    jsonData = metaData.data()
    return {"message": jsonData}