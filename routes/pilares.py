from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/pilares", tags=["Pilares"])

@router.post("/", response_model=schemas.Pilar)
def criar_pilar(pilar: schemas.PilarCreate, db: Session = Depends(database.get_db)):
    novo_pilar = models.Pilar(**pilar.dict())
    db.add(novo_pilar)
    db.commit()
    db.refresh(novo_pilar)
    return novo_pilar

@router.get("/", response_model=list[schemas.Pilar])
def listar_pilares(db: Session = Depends(database.get_db)):
    return db.query(models.Pilar).all()

@router.get("/{pilar_id}", response_model=schemas.Pilar)
def obter_pilar(pilar_id: int, db: Session = Depends(database.get_db)):
    pilar = db.query(models.Pilar).filter(models.Pilar.id == pilar_id).first()
    if not pilar:
        raise HTTPException(status_code=404, detail="Pilar não encontrado")
    return pilar

@router.put("/{pilar_id}", response_model=schemas.Pilar)
def atualizar_pilar(pilar_id: int, dados: schemas.PilarCreate, db: Session = Depends(database.get_db)):
    pilar = db.query(models.Pilar).filter(models.Pilar.id == pilar_id).first()
    if not pilar:
        raise HTTPException(status_code=404, detail="Pilar não encontrado")
    for key, value in dados.dict().items():
        setattr(pilar, key, value)
    db.commit()
    db.refresh(pilar)
    return pilar

@router.delete("/{pilar_id}")
def deletar_pilar(pilar_id: int, db: Session = Depends(database.get_db)):
    pilar = db.query(models.Pilar).filter(models.Pilar.id == pilar_id).first()
    if not pilar:
        raise HTTPException(status_code=404, detail="Pilar não encontrado")
    db.delete(pilar)
    db.commit()
    return {"mensagem": "Pilar deletado com sucesso"}
