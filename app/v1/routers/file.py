from fastapi import APIRouter
from fastapi.responses import FileResponse, ORJSONResponse, StreamingResponse, JSONResponse
from app.core.config import settings
import json
import io

router = APIRouter()


@router.get('/audio-cedict-normal')
async def audio(f: str):
   fx = settings._ROOT_PATH+"/app/v1/data/cedict/normal/"+f
   return FileResponse(fx, media_type='audio/mpeg')

@router.get('/json/stroke/{s}')
async def stroke(s: str):
   fx = settings._ROOT_PATH+"/app/v1/data/strokes/"+s
   with open(fx, 'r') as file:
         data = json.load(file)
   return JSONResponse(content=data)