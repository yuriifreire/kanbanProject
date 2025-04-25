from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models.column import Column
from ..schemas.column import ColumnCreate, Column, ColumnUpdate, ColumnWithCards

router = APIRouter(prefix="/columns", tags=["columns"])

@router.post("/", response_model=Column)
def create_column(column: ColumnCreate, db: Session = Depends(get_db)):
    db_column = Column(
        title=column.title,
        position=column.position,
        board_id=column.board_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_column)
    db.commit()
    db.refresh(db_column)
    return db_column

@router.get("/", response_model=List[Column])
def read_columns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Column).offset(skip).limit(limit).all()

@router.get("/{column_id}", response_model=ColumnWithCards)
def read_column(column_id: int, db: Session = Depends(get_db)):
    column = db.query(Column).filter(Column.id == column_id).first()
    if column is None:
        raise HTTPException(status_code=404, detail="Coluna não encontrada")
    return column

@router.put("/{column_id}", response_model=Column)
def update_column(column_id: int, column: ColumnUpdate, db: Session = Depends(get_db)):
    db_column = db.query(Column).filter(Column.id == column_id).first()
    if db_column is None:
        raise HTTPException(status_code=404, detail="Coluna não encontrada")
    
    update_data = column.dict(exclude_unset=True)
    update_data['updated_at'] = datetime.now()
    
    for field, value in update_data.items():
        setattr(db_column, field, value)
    
    db.commit()
    db.refresh(db_column)
    return db_column

@router.delete("/{column_id}")
def delete_column(column_id: int, db: Session = Depends(get_db)):
    db_column = db.query(Column).filter(Column.id == column_id).first()
    if db_column is None:
        raise HTTPException(status_code=404, detail="Coluna não encontrada")
    
    db.delete(db_column)
    db.commit()
    return {"message": "Coluna deletada com sucesso"}