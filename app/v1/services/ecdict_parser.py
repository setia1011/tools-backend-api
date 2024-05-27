import pandas as pd
import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, insert, desc, func, delete, text
from app.v1.models import Ecdict
from app.core.config import settings
import json


def ecdict_parse(db: Session = Depends):
   f = settings._ROOT_PATH+"/app/v1/data/stardict.csv"
   df1 = pd.read_csv(f, encoding='utf-8')
   df2 = df1.astype(object).where(df1.notna(), None)
   for i, r in df2.iterrows():
      db.execute(insert(Ecdict).values(
         word=r['word'],
         phonetic=r['phonetic'],
         definition=r['definition'],
         translation=r['translation'],
         pos=r['pos'],
         collins=r['collins'],
         oxford=r['oxford'],
         tag=r['tag'],
         bnc=r['bnc'],
         frq=r['frq'],
         exchange=r['exchange'],
         detail=r['detail'],
         audio=r['audio']
      ))
      db.commit()
