from gtts import gTTS
from io import BytesIO
from pypinyin import pinyin
from pypinyin.contrib.tone_convert import to_tone, to_finals, to_initials

import datetime
from pathlib import Path
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, insert, desc, func, delete, text, or_
from app.v1.models import Cedict
from pathlib import Path
from app.core.config import settings
import json


def cedict_parse(db: Session = Depends):
   list_of_dicts = []
   f = settings._ROOT_PATH+"/app/v1/data/cedict_ts.u8"

   with open(f, encoding='utf-8') as file:
      text = file.read()
      lines = text.split('\n')
      dict_lines = list(lines)

   def parse_line(line):
      parsed = {}
      if line == '':
         dict_lines.remove(line)
         return 0
      line = line.rstrip('/')
      line = line.split('/')
      if len(line) <= 1:
         return 0
      english = line[1]
      char_and_pinyin = line[0].split('[')
      if len(char_and_pinyin) < 2:
         return 0
      characters = char_and_pinyin[0].strip().split()
      if len(characters) < 2:
         return 0
      traditional = characters[0]
      simplified = characters[1]
      pinyinx = char_and_pinyin[1].rstrip(']').strip()
      parsed['traditional'] = traditional
      parsed['simplified'] = simplified
      parsed['pinyin'] = pinyinx.replace("]", "")
      parsed['english'] = english
      list_of_dicts.append(parsed)

   def remove_surnames():
      for x in range(len(list_of_dicts)-1, -1, -1):
         if "surname " in list_of_dicts[x]['english']:
            if x+1 < len(list_of_dicts) and list_of_dicts[x]['traditional'] == list_of_dicts[x+1]['traditional']:
                  list_of_dicts.pop(x)

   for line in dict_lines:
      parse_line(line)

   remove_surnames()

   for i in list_of_dicts:
      db.execute(insert(Cedict).values(traditional=i['traditional'], simplified=i['simplified'], pinyin=i['pinyin'], english=i['english']))
      db.commit()

def search_word(s: str, db: Session = Depends):
   # k = db.execute(select(Cedict).filter(or_(Cedict.simplified.like('%'+s), Cedict.traditional.like('%'+s))))
   k = db.execute(select(Cedict).filter(or_(Cedict.simplified==s, Cedict.traditional==s)))
   r = k.scalars().all()
   d = []
   for i in r:
      fn = settings._ROOT_PATH+"/app/v1/data/cedict/normal/"+i.simplified+".mp3"
      fs = settings._ROOT_PATH+"/app/v1/data/cedict/slow/"+i.simplified+".mp3"

      if Path(fn).exists():
         pass
      else: 
         tts_normal = gTTS(i.simplified, lang='zh-CN')
         tts_normal.save(fn)
      
      if Path(fs).exists():
         pass
      else: 
         tts_slow = gTTS(i.simplified, lang='zh-CN', slow=True)
         tts_slow.save(fs)

      d.append({
         "id": i.id,
         "traditional": i.traditional,
         "simplified": i.simplified,
         "pinyin": ' '.join(to_tone(a) for a in i.pinyin.split(' ')),
         "initials": [{a: to_initials(a.lower())} for a in i.pinyin.split(' ')],
         "finals": [{a: to_finals(a.lower())} for a in i.pinyin.split(' ')],
         "english": ' '.join(to_tone(a) if '[' in a or ']' in a else a for a in i.english.split(' ')),
         "audio_normal": i.audio_normal,
         "audio_slow": i.audio_slow,
         "updated_at": i.updated_at,
         "created_at": i.created_at
      })
   return d