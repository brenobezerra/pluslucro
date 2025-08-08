from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/formas-pagamento", tags=["Formas de Pagamento"])

@router.post("/", response_model=schemas.FormaPagamento)
def criar_forma_pagamento(forma: schemas.FormaPagamentoCreate, db: Session = Depends(database.get_db)):
    nova_forma = models.FormaPagamento(**forma.dict())
    db.add(nova_forma)
    db.commit()
    db.refresh(nova_forma)
    return nova_forma

@router.get("/", response_model=list[schemas.FormaPagamento])
def listar_formas_pagamento(db: Session = Depends(database.get_db)):
    return db.query(models.FormaPagamento).all()

@router.get("/{forma_id}", response_model=schemas.FormaPagamento)
def obter_forma_pagamento(forma_id: int, db: Session = Depends(database.get_db)):
    forma = db.query(models.FormaPagamento).filter(models.FormaPagamento.id == forma_id).first()
    if not forma:
        raise HTTPException(status_code=404, detail="Forma de pagamento não encontrada")
    return forma

@router.put("/{forma_id}", response_model=schemas.FormaPagamento)
def atualizar_forma_pagamento(forma_id: int, dados: schemas.FormaPagamentoCreate, db: Session = Depends(database.get_db)):
    forma = db.query(models.FormaPagamento).filter(models.FormaPagamento.id == forma_id).first()
    if not forma:
        raise HTTPException(status_code=404, detail="Forma de pagamento não encontrada")
    for key, value in dados.dict().items():
        setattr(forma, key, value)
    db.commit()
    db.refresh(forma)
    return forma

@router.delete("/{forma_id}")
def deletar_forma_pagamento(forma_id: int, db: Session = Depends(database.get_db)):
    forma = db.query(models.FormaPagamento).filter(models.FormaPagamento.id == forma_id).first()
    if not forma:
        raise HTTPException(status_code=404, detail="Forma de pagamento não encontrada")
    db.delete(forma)
    db.commit()
    return {"mensagem": "Forma de pagamento deletada com sucesso"}
