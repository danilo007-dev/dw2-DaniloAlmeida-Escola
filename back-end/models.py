# models.py
# Definição dos modelos ORM para SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

class StatusAlunoEnum(enum.Enum):
	ativo = "ativo"
	inativo = "inativo"

class Turma(Base):
	__tablename__ = "turmas"
	id = Column(Integer, primary_key=True, autoincrement=True)
	nome = Column(String(100), nullable=False)
	capacidade = Column(Integer, nullable=False)
	alunos = relationship("Aluno", back_populates="turma")

class Aluno(Base):
	__tablename__ = "alunos"
	id = Column(Integer, primary_key=True, autoincrement=True)
	nome = Column(String(100), nullable=False)
	data_nascimento = Column(Date, nullable=False)
	email = Column(String(120), nullable=True, unique=True)
	status = Column(Enum(StatusAlunoEnum), nullable=False, default=StatusAlunoEnum.inativo)
	turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=True)
	turma = relationship("Turma", back_populates="alunos")
