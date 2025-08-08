from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/subcategorias", tags=["Subcategorias"])

@router.post("/", response_model=schemas.Subcategoria)
def criar_subcategoria(sub: schemas.SubcategoriaCreate, db: Session = Depends(database.get_db)):
    nova_sub = models.Subcategoria(**sub.dict())
    db.add(nova_sub)
    db.commit()
    db.refresh(nova_sub)
    return nova_sub

@router.get("/", response_model=list[schemas.Subcategoria])
def listar_subcategorias(db: Session = Depends(database.get_db)):
    return db.query(models.Subcategoria).all()

@router.get("/{sub_id}", response_model=schemas.Subcategoria)
def obter_subcategoria(sub_id: int, db: Session = Depends(database.get_db)):
    sub = db.query(models.Subcategoria).filter(models.Subcategoria.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subcategoria não encontrada")
    return sub

@router.put("/{sub_id}", response_model=schemas.Subcategoria)
def atualizar_subcategoria(sub_id: int, dados: schemas.SubcategoriaCreate, db: Session = Depends(database.get_db)):
    sub = db.query(models.Subcategoria).filter(models.Subcategoria.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subcategoria não encontrada")
    for key, value in dados.dict().items():
        setattr(sub, key, value)
    db.commit()
    db.refresh(sub)
    return sub

@router.delete("/{sub_id}")
def deletar_subcategoria(sub_id: int, db: Session = Depends(database.get_db)):
    sub = db.query(models.Subcategoria).filter(models.Subcategoria.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subcategoria não encontrada")
    db.delete(sub)
    db.commit()
    return {"mensagem": "Subcategoria deletada com sucesso"}
