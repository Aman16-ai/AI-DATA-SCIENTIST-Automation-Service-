from fastapi import FastAPI
from schemas import GenerateCodePayload,ChartDataPayload
from metaData.main import MetaData
import json
# from LLM.Feature_Engineering.feature_eng import init
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from visulization.ChartsData import ChartData
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/fetchFileMetaData")
def fetchFileMetaData(paylaod: GenerateCodePayload):
    metaData = MetaData(paylaod.file_path)
    jsonData = metaData.data()
    return {"message": jsonData}

@app.post("/performFE")
def perFormFeatureEngineering(payload:GenerateCodePayload):
    # init(file_path=payload.file_path,query=payload.prompt)
    return {"message":"fe"}

@app.get("/chart/data")
def getChartData(payload:ChartDataPayload):
    chartData = ChartData(payload.file_path)
    return chartData.data(payload.x,payload.y)