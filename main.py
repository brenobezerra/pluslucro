from fastapi import FastAPI
from .database import engine, Base
from .routes import categorias, formas_pagamento, gastos, pilares, subcategorias, usuarios

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Gastos")

app.include_router(categorias.router)
app.include_router(formas_pagamento.router)
app.include_router(gastos.router)
app.include_router(pilares.router)
app.include_router(subcategorias.router)
app.include_router(usuarios.router)
