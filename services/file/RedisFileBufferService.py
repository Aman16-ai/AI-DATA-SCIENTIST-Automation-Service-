import base64
from fastapi import HTTPException


class RedisFileBufferService:

    def __init__(self,session_id:str,redisClient) -> None:
        self.session_id = session_id
        self.redis = redisClient
    async def getSessionFileBuffer(self):
        file_buffer_base64 = await self.redis.get(self.session_id)
        if not file_buffer_base64:
            raise HTTPException(status_code=404, detail="File data not found.")
        file_buffer = base64.b64decode(file_buffer_base64)
        return file_buffer