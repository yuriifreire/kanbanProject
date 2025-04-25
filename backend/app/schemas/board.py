from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .column import ColumnWithCards

class BoardBase(BaseModel):
    title: str
    description: Optional[str] = None

class BoardCreate(BoardBase):
    pass

class BoardUpdate(BoardBase):
    pass

class Board(BoardBase):
    id: int
    created_at: datetime
    updated_at: datetime
    columns: List[ColumnWithCards] = []

    class Config:
        orm_mode = True