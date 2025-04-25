from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CardBase(BaseModel):
    title: str
    description: Optional[str] = None
    position: int
    column_id: int

class CardCreate(CardBase):
    pass

class CardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    position: Optional[int] = None
    column_id: Optional[int] = None

class Card(CardBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True