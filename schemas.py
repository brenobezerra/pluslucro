from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    nome: str
    email: str

class UsuarioCreate(UsuarioBase):
    senha: str

class Usuario(UsuarioBase):
    id: int
    class Config:
        orm_mode = True

class CategoriaBase(BaseModel):
    nome: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    class Config:
        orm_mode = True

class SubcategoriaBase(BaseModel):
    nome: str
    categoria_id: int

class SubcategoriaCreate(SubcategoriaBase):
    pass

class Subcategoria(SubcategoriaBase):
    id: int
    class Config:
        orm_mode = True

class FormaPagamentoBase(BaseModel):
    nome: str

class FormaPagamentoCreate(FormaPagamentoBase):
    pass

class FormaPagamento(FormaPagamentoBase):
    id: int
    class Config:
        orm_mode = True

class PilarBase(BaseModel):
    nome: str

class PilarCreate(PilarBase):
    pass

class Pilar(PilarBase):
    id: int
    class Config:
        orm_mode = True

class GastoBase(BaseModel):
    descricao: str
    valor: float
    usuario_id: int
    categoria_id: Optional[int]
    subcategoria_id: Optional[int]
    forma_pagamento_id: Optional[int]
    pilar_id: Optional[int]

class GastoCreate(GastoBase):
    pass

class Gasto(GastoBase):
    id: int
    data: datetime
    class Config:
        orm_mode = True
