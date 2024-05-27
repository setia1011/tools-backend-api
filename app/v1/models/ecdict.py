from app.core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, TIMESTAMP, TEXT, text, FLOAT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Ecdict(Base):
   __tablename__ = "ecdict"

   id = Column(Integer, primary_key=True, index=True)
   word = Column(VARCHAR(500), index=True)
   phonetic = Column(VARCHAR(500), index=True)
   definition = Column(TEXT)
   translation = Column(TEXT)
   pos = Column(VARCHAR(500), index=True)
   collins = Column(FLOAT, index=True)
   oxford = Column(FLOAT, index=True)
   tag = Column(VARCHAR(500), index=True)
   bnc = Column(FLOAT, index=True)
   frq = Column(FLOAT, index=True)
   exchange = Column(VARCHAR(500), index=True)
   detail = Column(VARCHAR(500), index=True)
   audio = Column(FLOAT, index=True)

   created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
   updated_at = Column(TIMESTAMP(timezone=True), server_default=text("NULL ON UPDATE CURRENT_TIMESTAMP"))