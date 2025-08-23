from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 🔴 Troque pelos seus dados reais:
USUARIO = "postgres"
SENHA = "novasenha"
HOST = "localhost"
PORTA = "5432"
BANCO = "gastos_db"

DATABASE_URL = f"postgresql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para usar sessões em rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
