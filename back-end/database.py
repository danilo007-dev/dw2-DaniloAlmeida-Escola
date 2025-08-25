# database.py
# Configuração do banco de dados SQLite e SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'app.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
	DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
	Base.metadata.create_all(bind=engine)
