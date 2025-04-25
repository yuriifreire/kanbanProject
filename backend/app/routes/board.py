from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models.board import Board
from ..models.column import Column
from ..schemas.board import BoardCreate, Board, BoardUpdate

router = APIRouter(prefix="/boards", tags=["boards"])

@router.post("/", response_model=Board)
def create_board(board: BoardCreate, db: Session = Depends(get_db)):
    db_board = Board(
        title=board.title,
        description=board.description,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

@router.get("/", response_model=List[Board])
def read_boards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Board).offset(skip).limit(limit).all()

@router.get("/{board_id}", response_model=Board)
def read_board(board_id: int, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if board is None:
        raise HTTPException(status_code=404, detail="Quadro não encontrado")
    return board

@router.put("/{board_id}", response_model=Board)
def update_board(board_id: int, board: BoardUpdate, db: Session = Depends(get_db)):
    db_board = db.query(Board).filter(Board.id == board_id).first()
    if db_board is None:
        raise HTTPException(status_code=404, detail="Quadro não encontrado")
    
    update_data = board.dict(exclude_unset=True)
    update_data['updated_at'] = datetime.now()
    
    for field, value in update_data.items():
        setattr(db_board, field, value)
    
    db.commit()
    db.refresh(db_board)
    return db_board

@router.delete("/{board_id}")
def delete_board(board_id: int, db: Session = Depends(get_db)):
    db_board = db.query(Board).filter(Board.id == board_id).first()
    if db_board is None:
        raise HTTPException(status_code=404, detail="Quadro não encontrado")
    
    db.delete(db_board)
    db.commit()
    return {"message": "Quadro deletado com sucesso"}