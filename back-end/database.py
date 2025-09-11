# database.py
# Configuração do banco de dados SQLite e SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base
import os
from typing import Generator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'escola.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Configuração do engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False  # Mude para True para ver as queries SQL
)

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """Cria o banco de dados e todas as tabelas"""
    print("🗄️ Criando banco de dados e tabelas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados criado com sucesso!")

def get_database_session() -> Generator[Session, None, None]:
    """
    Dependency para obter uma sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def init_database():
    """Inicializa o banco de dados"""
    # Verifica se o banco já existe
    if not os.path.exists(DB_PATH):
        print("🔧 Banco de dados não encontrado. Criando...")
        create_db_and_tables()
    else:
        print("📋 Banco de dados encontrado!")
    
    return engine
