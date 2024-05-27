from app.core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, TIMESTAMP, TEXT, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Cedict(Base):
   __tablename__ = "cedict"

   id = Column(Integer, primary_key=True, index=True)
   traditional = Column(VARCHAR(500), index=True)
   simplified = Column(VARCHAR(500), index=True)
   pinyin = Column(VARCHAR(500), index=True)
   english = Column(TEXT)
   audio_normal = Column(VARCHAR(500), index=True)
   audio_slow = Column(VARCHAR(500), index=True)

   created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
   updated_at = Column(TIMESTAMP(timezone=True), server_default=text("NULL ON UPDATE CURRENT_TIMESTAMP"))