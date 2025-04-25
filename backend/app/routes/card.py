from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models.card import Card
from ..models.column import Column
from ..schemas.card import CardCreate, Card, CardUpdate

router = APIRouter(prefix="/cards", tags=["cards"])

@router.post("/", response_model=Card)
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    # Verifica se a coluna existe
    db_column = db.query(Column).filter(Column.id == card.column_id).first()
    if db_column is None:
        raise HTTPException(status_code=404, detail="Coluna não encontrada")
    
    db_card = Card(
        title=card.title,
        description=card.description,
        position=card.position,
        column_id=card.column_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

@router.get("/", response_model=List[Card])
def read_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Card).offset(skip).limit(limit).all()

@router.get("/{card_id}", response_model=Card)
def read_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card não encontrado")
    return card

@router.put("/{card_id}", response_model=Card)
def update_card(card_id: int, card: CardUpdate, db: Session = Depends(get_db)):
    db_card = db.query(Card).filter(Card.id == card_id).first()
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card não encontrado")
    
    # Verifica se a nova coluna existe (se for atualização)
    if card.column_id is not None:
        db_column = db.query(Column).filter(Column.id == card.column_id).first()
        if db_column is None:
            raise HTTPException(status_code=404, detail="Não foi possível achar a nova coluna")
    
    update_data = card.dict(exclude_unset=True)
    update_data['updated_at'] = datetime.now()
    
    for field, value in update_data.items():
        setattr(db_card, field, value)
    
    db.commit()
    db.refresh(db_card)
    return db_card

@router.delete("/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db)):
    db_card = db.query(Card).filter(Card.id == card_id).first()
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card não encontrado")
    
    db.delete(db_card)
    db.commit()
    return {"message": "Card deletado com sucesso"}

@router.post("/{card_id}/move", response_model=Card)
def move_card(
    card_id: int, 
    new_column_id: int, 
    new_position: int, 
    db: Session = Depends(get_db)
):
    db_card = db.query(Card).filter(Card.id == card_id).first()
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card não encontrado")
    
    db_column = db.query(Column).filter(Column.id == new_column_id).first()
    if db_column is None:
        raise HTTPException(status_code=404, detail="Coluna não encontrada")
    
    # Atualiza a posição dos outros cards na coluna de destino
    if db_card.column_id != new_column_id:
        # Ajusta posições na coluna de origem
        db.query(Card)\
            .filter(Card.column_id == db_card.column_id,
                    Card.position > db_card.position)\
            .update({Card.position: Card.position - 1})
    
    # Ajusta posições na coluna de destino
    db.query(Card)\
        .filter(Card.column_id == new_column_id,
                Card.position >= new_position)\
        .update({Card.position: Card.position + 1})
    
    # Move o card
    db_card.column_id = new_column_id
    db_card.position = new_position
    db_card.updated_at = datetime.now()
    
    db.commit()
    db.refresh(db_card)
    return db_card