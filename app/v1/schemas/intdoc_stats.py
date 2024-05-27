import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Union


class MyBaseModel(BaseModel):
    class Config:
        model_config = ConfigDict(from_attributes=True)

class ChartKomposisi(MyBaseModel):
    value: str
    label: str