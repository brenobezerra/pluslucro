from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/gastos", tags=["Gastos"])

@router.post("/", response_model=schemas.Gasto)
def criar_gasto(gasto: schemas.GastoCreate, db: Session = Depends(database.get_db)):
    novo_gasto = models.Gasto(**gasto.dict())
    db.add(novo_gasto)
    db.commit()
    db.refresh(novo_gasto)
    return novo_gasto

@router.get("/", response_model=list[schemas.Gasto])
def listar_gastos(db: Session = Depends(database.get_db)):
    return db.query(models.Gasto).all()

@router.get("/{gasto_id}", response_model=schemas.Gasto)
def obter_gasto(gasto_id: int, db: Session = Depends(database.get_db)):
    gasto = db.query(models.Gasto).filter(models.Gasto.id == gasto_id).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")
    return gasto

@router.put("/{gasto_id}", response_model=schemas.Gasto)
def atualizar_gasto(gasto_id: int, dados: schemas.GastoCreate, db: Session = Depends(database.get_db)):
    gasto = db.query(models.Gasto).filter(models.Gasto.id == gasto_id).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")
    for key, value in dados.dict().items():
        setattr(gasto, key, value)
    db.commit()
    db.refresh(gasto)
    return gasto

@router.delete("/{gasto_id}")
def deletar_gasto(gasto_id: int, db: Session = Depends(database.get_db)):
    gasto = db.query(models.Gasto).filter(models.Gasto.id == gasto_id).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")
    db.delete(gasto)
    db.commit()
    return {"mensagem": "Gasto deletado com sucesso"}
