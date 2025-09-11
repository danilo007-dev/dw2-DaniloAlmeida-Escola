# models.py
# Definição dos modelos ORM para SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, DateTime, Boolean, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class StatusAlunoEnum(enum.Enum):
    ativo = "ativo"
    inativo = "inativo"

class CargoEnum(enum.Enum):
    diretor = "diretor"
    coordenador = "coordenador"
    secretario = "secretario"
    professor = "professor"

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)
    senha_hash = Column(String(255), nullable=False)
    cargo = Column(Enum(CargoEnum), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    data_criacao = Column(DateTime, default=func.now(), nullable=False)
    ultimo_acesso = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Usuario(id={self.id}, nome='{self.nome}', email='{self.email}', cargo='{self.cargo.value}')>"

class Turma(Base):
    __tablename__ = "turmas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    descricao = Column(Text, nullable=True)
    capacidade = Column(Integer, nullable=False, default=30)
    ano_letivo = Column(String(10), nullable=False)
    periodo = Column(String(20), nullable=True)  # manhã, tarde, noite
    ativa = Column(Boolean, default=True, nullable=False)
    data_criacao = Column(DateTime, default=func.now(), nullable=False)
    
    # Relacionamento com alunos
    alunos = relationship("Aluno", back_populates="turma", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Turma(id={self.id}, nome='{self.nome}', capacidade={self.capacidade})>"

class Aluno(Base):
    __tablename__ = "alunos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, index=True)
    cpf = Column(String(14), nullable=True, unique=True)  # Format: 000.000.000-00
    rg = Column(String(20), nullable=True)
    data_nascimento = Column(Date, nullable=False)
    email = Column(String(120), nullable=True, unique=True)
    telefone = Column(String(20), nullable=True)
    endereco = Column(Text, nullable=True)
    nome_responsavel = Column(String(100), nullable=True)
    telefone_responsavel = Column(String(20), nullable=True)
    status = Column(Enum(StatusAlunoEnum), nullable=False, default=StatusAlunoEnum.ativo)
    data_matricula = Column(Date, nullable=True)
    data_criacao = Column(DateTime, default=func.now(), nullable=False)
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    observacoes = Column(Text, nullable=True)
    
    # Relacionamento com turma
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=True)
    turma = relationship("Turma", back_populates="alunos")
    
    def __repr__(self):
        return f"<Aluno(id={self.id}, nome='{self.nome}', status='{self.status.value}')>"

class HistoricoLogin(Base):
    __tablename__ = "historico_login"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    data_login = Column(DateTime, default=func.now(), nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    sucesso = Column(Boolean, nullable=False)
    
    # Relacionamento
    usuario = relationship("Usuario")
    
    def __repr__(self):
        return f"<HistoricoLogin(usuario_id={self.usuario_id}, data='{self.data_login}', sucesso={self.sucesso})>"
