from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    gastos = relationship("Gasto", back_populates="usuario")

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    subcategorias = relationship("Subcategoria", back_populates="categoria")

class Subcategoria(Base):
    __tablename__ = "subcategorias"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria", back_populates="subcategorias")
    gastos = relationship("Gasto", back_populates="subcategoria")

class FormaPagamento(Base):
    __tablename__ = "formas_pagamento"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    gastos = relationship("Gasto", back_populates="forma_pagamento")

class Pilar(Base):
    __tablename__ = "pilares"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    gastos = relationship("Gasto", back_populates="pilar")

class Gasto(Base):
    __tablename__ = "gastos"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    subcategoria_id = Column(Integer, ForeignKey("subcategorias.id"))
    forma_pagamento_id = Column(Integer, ForeignKey("formas_pagamento.id"))
    pilar_id = Column(Integer, ForeignKey("pilares.id"))

    usuario = relationship("Usuario", back_populates="gastos")
    subcategoria = relationship("Subcategoria", back_populates="gastos")
    forma_pagamento = relationship("FormaPagamento", back_populates="gastos")
    pilar = relationship("Pilar", back_populates="gastos")
