from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.database import db_sync_session
from app.core.config import settings
from app.v1.services import ecdict_parser
import json

router = APIRouter()

@router.get("/ecdict-parse", name="Parse CEDICT", description="Parse CEDICT")
def cedict_parse(db: Session = Depends(db_sync_session)):
   try:
      ecdict_parser.ecdict_parse(db=db)
   except:
      raise