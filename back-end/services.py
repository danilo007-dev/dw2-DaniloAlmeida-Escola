# services.py
# Lógica de negócio e operações de banco de dados
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc, func
from models import Usuario, Aluno, Turma, HistoricoLogin, StatusAlunoEnum, CargoEnum
from schemas import (
    UsuarioCreate, UsuarioUpdate, AlunoCreate, AlunoUpdate, 
    TurmaCreate, TurmaUpdate, AlunoResponse, TurmaResponse
)
from auth import get_password_hash
from typing import List, Optional, Tuple
from datetime import date, datetime
from fastapi import HTTPException, status

class UsuarioService:
    @staticmethod
    def create_user(db: Session, user_data: UsuarioCreate) -> Usuario:
        """Cria um novo usuário"""
        # Verificar se email já existe
        existing_user = db.query(Usuario).filter(Usuario.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado no sistema"
            )
        
        # Criar usuário
        db_user = Usuario(
            nome=user_data.nome,
            email=user_data.email,
            senha_hash=get_password_hash(user_data.senha),
            cargo=user_data.cargo,
            ativo=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[Usuario]:
        """Busca usuário por ID"""
        return db.query(Usuario).filter(Usuario.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[Usuario]:
        """Busca usuário por email"""
        return db.query(Usuario).filter(Usuario.email == email).first()
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> Tuple[List[Usuario], int]:
        """Lista usuários com paginação"""
        total = db.query(Usuario).count()
        users = db.query(Usuario).offset(skip).limit(limit).all()
        return users, total
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UsuarioUpdate) -> Usuario:
        """Atualiza usuário"""
        db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        for field, value in user_data.dict(exclude_unset=True).items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update_last_access(db: Session, user_id: int):
        """Atualiza último acesso do usuário"""
        db.query(Usuario).filter(Usuario.id == user_id).update({
            "ultimo_acesso": datetime.utcnow()
        })
        db.commit()

class TurmaService:
    @staticmethod
    def create_turma(db: Session, turma_data: TurmaCreate) -> Turma:
        """Cria nova turma"""
        # Verificar se nome já existe
        existing_turma = db.query(Turma).filter(Turma.nome == turma_data.nome).first()
        if existing_turma:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma turma com este nome"
            )
        
        db_turma = Turma(**turma_data.dict())
        db.add(db_turma)
        db.commit()
        db.refresh(db_turma)
        return db_turma
    
    @staticmethod
    def get_turma_by_id(db: Session, turma_id: int) -> Optional[Turma]:
        """Busca turma por ID"""
        return db.query(Turma).filter(Turma.id == turma_id).first()
    
    @staticmethod
    def get_turmas(db: Session, skip: int = 0, limit: int = 100, ativas_apenas: bool = True) -> Tuple[List[Turma], int]:
        """Lista turmas com paginação"""
        query = db.query(Turma)
        if ativas_apenas:
            query = query.filter(Turma.ativa == True)
        
        total = query.count()
        turmas = query.order_by(Turma.nome).offset(skip).limit(limit).all()
        return turmas, total
    
    @staticmethod
    def get_turmas_with_stats(db: Session) -> List[TurmaResponse]:
        """Lista turmas com estatísticas de alunos"""
        turmas = db.query(Turma).filter(Turma.ativa == True).all()
        result = []
        
        for turma in turmas:
            total_alunos = db.query(Aluno).filter(
                Aluno.turma_id == turma.id,
                Aluno.status == StatusAlunoEnum.ativo
            ).count()
            
            turma_response = TurmaResponse(
                id=turma.id,
                nome=turma.nome,
                descricao=turma.descricao,
                capacidade=turma.capacidade,
                ano_letivo=turma.ano_letivo,
                periodo=turma.periodo,
                ativa=turma.ativa,
                data_criacao=turma.data_criacao,
                total_alunos=total_alunos
            )
            result.append(turma_response)
        
        return result
    
    @staticmethod
    def update_turma(db: Session, turma_id: int, turma_data: TurmaUpdate) -> Turma:
        """Atualiza turma"""
        db_turma = db.query(Turma).filter(Turma.id == turma_id).first()
        if not db_turma:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Turma não encontrada"
            )
        
        for field, value in turma_data.dict(exclude_unset=True).items():
            setattr(db_turma, field, value)
        
        db.commit()
        db.refresh(db_turma)
        return db_turma
    
    @staticmethod
    def delete_turma(db: Session, turma_id: int) -> bool:
        """Desativa turma (soft delete)"""
        db_turma = db.query(Turma).filter(Turma.id == turma_id).first()
        if not db_turma:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Turma não encontrada"
            )
        
        # Verificar se há alunos na turma
        alunos_count = db.query(Aluno).filter(
            Aluno.turma_id == turma_id,
            Aluno.status == StatusAlunoEnum.ativo
        ).count()
        
        if alunos_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Não é possível excluir turma com {alunos_count} aluno(s) ativo(s)"
            )
        
        db_turma.ativa = False
        db.commit()
        return True

class AlunoService:
    @staticmethod
    def create_aluno(db: Session, aluno_data: AlunoCreate) -> Aluno:
        """Cria novo aluno"""
        # Verificar se email já existe
        if aluno_data.email:
            existing_aluno = db.query(Aluno).filter(Aluno.email == aluno_data.email).first()
            if existing_aluno:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado para outro aluno"
                )
        
        # Verificar se CPF já existe
        if aluno_data.cpf:
            existing_cpf = db.query(Aluno).filter(Aluno.cpf == aluno_data.cpf).first()
            if existing_cpf:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CPF já cadastrado para outro aluno"
                )
        
        # Verificar se turma existe e tem capacidade
        if aluno_data.turma_id:
            turma = db.query(Turma).filter(Turma.id == aluno_data.turma_id).first()
            if not turma:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Turma não encontrada"
                )
            
            alunos_na_turma = db.query(Aluno).filter(
                Aluno.turma_id == aluno_data.turma_id,
                Aluno.status == StatusAlunoEnum.ativo
            ).count()
            
            if alunos_na_turma >= turma.capacidade:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Turma já atingiu capacidade máxima"
                )
        
        db_aluno = Aluno(**aluno_data.dict())
        db.add(db_aluno)
        db.commit()
        db.refresh(db_aluno)
        return db_aluno
    
    @staticmethod
    def get_aluno_by_id(db: Session, aluno_id: int) -> Optional[Aluno]:
        """Busca aluno por ID"""
        return db.query(Aluno).filter(Aluno.id == aluno_id).first()
    
    @staticmethod
    def get_alunos(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        turma_id: Optional[int] = None,
        status: Optional[StatusAlunoEnum] = None
    ) -> Tuple[List[Aluno], int]:
        """Lista alunos com filtros e paginação"""
        query = db.query(Aluno)
        
        # Filtros
        if search:
            query = query.filter(
                or_(
                    Aluno.nome.contains(search),
                    Aluno.email.contains(search) if search else False
                )
            )
        
        if turma_id:
            query = query.filter(Aluno.turma_id == turma_id)
        
        if status:
            query = query.filter(Aluno.status == status)
        
        total = query.count()
        alunos = query.order_by(Aluno.nome).offset(skip).limit(limit).all()
        return alunos, total
    
    @staticmethod
    def get_alunos_with_turma(db: Session) -> List[AlunoResponse]:
        """Lista alunos com informações da turma"""
        alunos = db.query(Aluno).join(Turma, Aluno.turma_id == Turma.id, isouter=True).all()
        result = []
        
        for aluno in alunos:
            # Calcular idade
            today = date.today()
            idade = today.year - aluno.data_nascimento.year - ((today.month, today.day) < (aluno.data_nascimento.month, aluno.data_nascimento.day))
            
            aluno_response = AlunoResponse(
                id=aluno.id,
                nome=aluno.nome,
                cpf=aluno.cpf,
                rg=aluno.rg,
                data_nascimento=aluno.data_nascimento,
                email=aluno.email,
                telefone=aluno.telefone,
                endereco=aluno.endereco,
                nome_responsavel=aluno.nome_responsavel,
                telefone_responsavel=aluno.telefone_responsavel,
                status=aluno.status,
                data_matricula=aluno.data_matricula,
                observacoes=aluno.observacoes,
                turma_id=aluno.turma_id,
                data_criacao=aluno.data_criacao,
                data_atualizacao=aluno.data_atualizacao,
                turma_nome=aluno.turma.nome if aluno.turma else None,
                idade=idade
            )
            result.append(aluno_response)
        
        return result
    
    @staticmethod
    def update_aluno(db: Session, aluno_id: int, aluno_data: AlunoUpdate) -> Aluno:
        """Atualiza aluno"""
        db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if not db_aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado"
            )
        
        # Verificar conflitos apenas se os campos estão sendo alterados
        update_data = aluno_data.dict(exclude_unset=True)
        
        if 'email' in update_data and update_data['email']:
            existing_aluno = db.query(Aluno).filter(
                Aluno.email == update_data['email'],
                Aluno.id != aluno_id
            ).first()
            if existing_aluno:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado para outro aluno"
                )
        
        if 'cpf' in update_data and update_data['cpf']:
            existing_cpf = db.query(Aluno).filter(
                Aluno.cpf == update_data['cpf'],
                Aluno.id != aluno_id
            ).first()
            if existing_cpf:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CPF já cadastrado para outro aluno"
                )
        
        for field, value in update_data.items():
            setattr(db_aluno, field, value)
        
        db.commit()
        db.refresh(db_aluno)
        return db_aluno
    
    @staticmethod
    def delete_aluno(db: Session, aluno_id: int) -> dict:
        """Inativa aluno (soft delete) ou exclui permanentemente se já inativo"""
        db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if not db_aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado"
            )
        
        # Se o aluno já está inativo, exclui permanentemente
        if db_aluno.status == StatusAlunoEnum.inativo:
            db.delete(db_aluno)
            db.commit()
            return {"action": "deleted", "message": "Aluno excluído permanentemente"}
        
        # Se o aluno está ativo, apenas inativa (soft delete)
        db_aluno.status = StatusAlunoEnum.inativo
        db.commit()
        return {"action": "inactivated", "message": "Aluno inativado com sucesso"}

class StatisticsService:
    @staticmethod
    def get_dashboard_stats(db: Session) -> dict:
        """Retorna estatísticas para o dashboard"""
        # Contadores básicos
        total_alunos = db.query(Aluno).count()
        alunos_ativos = db.query(Aluno).filter(Aluno.status == StatusAlunoEnum.ativo).count()
        alunos_inativos = total_alunos - alunos_ativos
        
        total_turmas = db.query(Turma).count()
        turmas_ativas = db.query(Turma).filter(Turma.ativa == True).count()
        
        usuarios_ativos = db.query(Usuario).filter(Usuario.ativo == True).count()
        
        # Alunos por turma
        alunos_por_turma = db.query(
            Turma.nome,
            func.count(Aluno.id).label('total')
        ).join(
            Aluno, Turma.id == Aluno.turma_id, isouter=True
        ).filter(
            Turma.ativa == True
        ).group_by(Turma.id, Turma.nome).all()
        
        alunos_por_turma_list = [
            {"turma": nome, "total": total}
            for nome, total in alunos_por_turma
        ]
        
        return {
            "total_alunos": total_alunos,
            "alunos_ativos": alunos_ativos,
            "alunos_inativos": alunos_inativos,
            "total_turmas": total_turmas,
            "turmas_ativas": turmas_ativas,
            "alunos_por_turma": alunos_por_turma_list,
            "usuarios_ativos": usuarios_ativos
        }
