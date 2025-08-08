from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.post("/", response_model=schemas.Categoria)
def criar_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(database.get_db)):
    nova_categoria = models.Categoria(**categoria.dict())
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria

@router.get("/", response_model=list[schemas.Categoria])
def listar_categorias(db: Session = Depends(database.get_db)):
    return db.query(models.Categoria).all()

@router.get("/{categoria_id}", response_model=schemas.Categoria)
def obter_categoria(categoria_id: int, db: Session = Depends(database.get_db)):
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

@router.put("/{categoria_id}", response_model=schemas.Categoria)
def atualizar_categoria(categoria_id: int, dados: schemas.CategoriaCreate, db: Session = Depends(database.get_db)):
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    for key, value in dados.dict().items():
        setattr(categoria, key, value)
    db.commit()
    db.refresh(categoria)
    return categoria

@router.delete("/{categoria_id}")
def deletar_categoria(categoria_id: int, db: Session = Depends(database.get_db)):
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    db.delete(categoria)
    db.commit()
    return {"mensagem": "Categoria deletada com sucesso"}
