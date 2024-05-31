from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.database import db_sync_session
from app.core.config import settings
from app.v1.services import cedict_parser
import json

router = APIRouter()

@router.get("/cedict-parse", name="Parse CEDICT", description="Parse CEDICT")
def cedict_parse(db: Session = Depends(db_sync_session)):
   try:
      cedict_parser.cedict_parse(db=db)
   except:
      raise

@router.get('/search-word')
def search_word(s: str, db: Session = Depends(db_sync_session)):
   try:
      return cedict_parser.search_word(s=s, db=db)
   except:
      raise

@router.get('/pinyin')
def pinyin(s: str):
   try:
      return cedict_parser.goPinyin(s=s)
   except:
      raise