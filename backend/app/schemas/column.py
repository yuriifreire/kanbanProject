from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .card import Card

class ColumnBase(BaseModel):
    title: str
    position: int
    board_id: int

class ColumnCreate(ColumnBase):
    pass

class ColumnUpdate(BaseModel):
    title: Optional[str] = None
    position: Optional[int] = None

class Column(ColumnBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ColumnWithCards(Column):
    cards: List[Card] = []