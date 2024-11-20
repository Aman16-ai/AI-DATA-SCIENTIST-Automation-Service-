from fastapi import FastAPI, Request,Response
from schemas import GenerateCodePayload,ChartDataPayload,metaDataFilePayloads
from metaData.main import MetaData
import json
from featureEngineering import main
# from LLM.Feature_Engineering.feature_eng import init
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from visulization.ChartsData import ChartData
from redis import asyncio
import json
from settings import UPLOAD_DIR
import pandas as pd
from utils.DataFrameUtils import parseDataFrameToJson
import os


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv('CLIENT_ORIGIN_URL','http://localhost:5173')],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




async def redis_pool():
    # Redis client bound to pool of connections (auto-reconnecting).
    return asyncio.from_url(
        os.getenv("REDIS_URL"), encoding="utf-8", decode_responses=True
    )

@app.on_event("startup")
async def create_redis():
    app.state.redis = await redis_pool()


@app.on_event("shutdown")
async def close_redis():
    await app.state.redis.close()


import os
os.makedirs(UPLOAD_DIR,exist_ok=True)
@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post("/performFE")
def perFormFeatureEngineering(payload:GenerateCodePayload):
    # init(file_path=payload.file_path,query=payload.prompt)
    file = 'test_df.csv'
    query = "give the rows with salary greater than 65000"
    response = main.performFeatureEngineering(payload.file_path,payload.prompt,userId=payload.userId)
    return {"message":response}


import base64
from fastapi import HTTPException


class RedisFileBufferService:

    def __init__(self,session_id:str,redisClient) -> None:
        self.session_id = session_id
        self.redis = redisClient


    async def getSessionFileBuffer(self):
        data = await self.redis.get(self.session_id)
        if not data:
            raise HTTPException(status_code=404, detail="File data not found.")
        
        file_data = json.loads(data)
        buffer_base64 = file_data.get('fileBuffer')

        if not buffer_base64:
            raise HTTPException(status_code=400, detail="Invalid file data")
        
        file_buffer = base64.b64decode(buffer_base64)
        return file_buffer
    

@app.post("/chart/data")
async def getChartData(chartDataPayload:ChartDataPayload):
    session_id = chartDataPayload.sessionId
    print(session_id)
    if session_id is None:
        return {"Error":"session not found"}
    fileservice = RedisFileBufferService(session_id,app.state.redis)
    buffer = await fileservice.getSessionFileBuffer()
    chartData = ChartData(buffer)
    result = chartData.data(chartDataPayload.x['value'],chartDataPayload.x['type'],chartDataPayload.y['value'],chartDataPayload.y['type'])
    # chartData = ChartData(payload.file_path)\
    print(result)
    # parsed = parseDataFrameToJson(result)
    return {'noi':result.to_dict()}


@app.get("/fetchFileMetaData/{session_id}")
async def fetchFileMetaData(session_id:str):
    print(session_id)
    if session_id is None:
        return {"Error":"session not found"}
    fileservice = RedisFileBufferService(session_id,app.state.redis)
    buffer = await fileservice.getSessionFileBuffer()
    print(buffer)
    metaData = MetaData(buffer)
    jsonData = metaData.data()
    return {"message": jsonData}