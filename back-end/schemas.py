# schemas.py
# Schemas Pydantic para validação de dados
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

# Enums
class StatusAlunoEnum(str, Enum):
    ativo = "ativo"
    inativo = "inativo"

class CargoEnum(str, Enum):
    diretor = "diretor"
    coordenador = "coordenador"
    secretario = "secretario"
    professor = "professor"

# Schemas de Usuario
class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    cargo: CargoEnum

class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=6)
    
    @validator('nome')
    def validate_nome(cls, v):
        if not v.strip():
            raise ValueError('Nome não pode estar vazio')
        return v.strip().title()

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int
    ativo: bool
    data_criacao: datetime
    ultimo_acesso: Optional[datetime]
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, obj):
        """Converter ORM object para response, garantindo que enum seja string"""
        cargo_value = obj.cargo.value if hasattr(obj.cargo, 'value') else str(obj.cargo)
        return cls(
            id=obj.id,
            nome=obj.nome,
            email=obj.email,
            cargo=cargo_value,
            ativo=obj.ativo,
            data_criacao=obj.data_criacao,
            ultimo_acesso=obj.ultimo_acesso
        )

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    cargo: Optional[CargoEnum] = None
    ativo: Optional[bool] = None

# Schemas de Turma
class TurmaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: Optional[str] = None
    capacidade: int = Field(..., ge=1, le=100)
    ano_letivo: str = Field(..., min_length=4, max_length=10)
    periodo: Optional[str] = None

class TurmaCreate(TurmaBase):
    @validator('nome')
    def validate_nome(cls, v):
        if not v.strip():
            raise ValueError('Nome da turma não pode estar vazio')
        return v.strip().upper()
    
    @validator('ano_letivo')
    def validate_ano_letivo(cls, v):
        try:
            year = int(v)
            if year < 2020 or year > 2030:
                raise ValueError('Ano letivo deve estar entre 2020 e 2030')
        except ValueError:
            raise ValueError('Ano letivo deve ser um número válido')
        return v

class TurmaResponse(TurmaBase):
    id: int
    ativa: bool
    data_criacao: datetime
    total_alunos: int = 0
    
    class Config:
        from_attributes = True

class TurmaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    descricao: Optional[str] = None
    capacidade: Optional[int] = Field(None, ge=1, le=100)
    ano_letivo: Optional[str] = Field(None, min_length=4, max_length=10)
    periodo: Optional[str] = None
    ativa: Optional[bool] = None

# Schemas de Aluno
class AlunoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    cpf: Optional[str] = None
    rg: Optional[str] = None
    data_nascimento: date
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    nome_responsavel: Optional[str] = None
    telefone_responsavel: Optional[str] = None
    status: StatusAlunoEnum = StatusAlunoEnum.ativo
    data_matricula: Optional[date] = None
    observacoes: Optional[str] = None
    turma_id: Optional[int] = None

class AlunoCreate(AlunoBase):
    @validator('nome')
    def validate_nome(cls, v):
        if not v.strip():
            raise ValueError('Nome não pode estar vazio')
        return v.strip().title()
    
    @validator('cpf')
    def validate_cpf(cls, v):
        if v:
            # Remove caracteres especiais
            cpf_numbers = ''.join(filter(str.isdigit, v))
            if len(cpf_numbers) != 11:
                raise ValueError('CPF deve ter 11 dígitos')
            # Formatar CPF
            return f"{cpf_numbers[:3]}.{cpf_numbers[3:6]}.{cpf_numbers[6:9]}-{cpf_numbers[9:]}"
        return v
    
    @validator('data_nascimento')
    def validate_data_nascimento(cls, v):
        today = date.today()
        if v > today:
            raise ValueError('Data de nascimento não pode ser no futuro')
        
        # Calcular idade
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age > 100:
            raise ValueError('Idade não pode ser superior a 100 anos')
        
        return v

class AlunoResponse(AlunoBase):
    id: int
    data_criacao: datetime
    data_atualizacao: datetime
    turma_nome: Optional[str] = None
    idade: Optional[int] = None
    
    class Config:
        from_attributes = True

class AlunoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    cpf: Optional[str] = None
    rg: Optional[str] = None
    data_nascimento: Optional[date] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    nome_responsavel: Optional[str] = None
    telefone_responsavel: Optional[str] = None
    status: Optional[StatusAlunoEnum] = None
    data_matricula: Optional[date] = None
    observacoes: Optional[str] = None
    turma_id: Optional[int] = None

# Schemas de Resposta
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UsuarioResponse

class MessageResponse(BaseModel):
    message: str
    success: bool = True

class StatisticsResponse(BaseModel):
    total_alunos: int
    alunos_ativos: int
    alunos_inativos: int
    total_turmas: int
    turmas_ativas: int
    alunos_por_turma: List[dict]
    usuarios_ativos: int

# Schemas para listas com paginação
class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    size: int
    pages: int

class AlunoListResponse(PaginatedResponse):
    items: List[AlunoResponse]

class TurmaListResponse(PaginatedResponse):
    items: List[TurmaResponse]

class UsuarioListResponse(PaginatedResponse):
    items: List[UsuarioResponse]
