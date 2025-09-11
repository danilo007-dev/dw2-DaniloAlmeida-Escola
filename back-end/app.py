# app.py
# Aplicação FastAPI principal com todas as rotas
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta
import uvicorn

# Imports locais
from database import get_database_session, init_database
from models import Usuario, Aluno, Turma, HistoricoLogin
from schemas import (
    UsuarioCreate, UsuarioLogin, UsuarioResponse, UsuarioUpdate,
    AlunoCreate, AlunoUpdate, AlunoResponse, AlunoListResponse,
    TurmaCreate, TurmaUpdate, TurmaResponse, TurmaListResponse,
    TokenResponse, MessageResponse, StatisticsResponse
)
from auth import (
    authenticate_user, create_access_token, get_current_user,
    require_admin, require_admin_or_coordinator, ACCESS_TOKEN_EXPIRE_MINUTES
)
from services import UsuarioService, AlunoService, TurmaService, StatisticsService

# Inicializar aplicação
app = FastAPI(
    title="🎓 Sistema de Gestão Escolar API",
    description="API completa para gerenciamento de escola com autenticação JWT",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar banco de dados na inicialização
@app.on_event("startup")
async def startup_event():
    """Eventos de inicialização"""
    print("🚀 Iniciando Sistema de Gestão Escolar...")
    init_database()
    print("✅ Sistema pronto para uso!")

# ================================
# ROTAS DE AUTENTICAÇÃO
# ================================

@app.post("/auth/register", response_model=MessageResponse, tags=["Autenticação"])
async def register_user(
    user_data: UsuarioCreate,
    db: Session = Depends(get_database_session)
):
    """Registrar novo usuário"""
    try:
        user = UsuarioService.create_user(db, user_data)
        return MessageResponse(
            message=f"Usuário {user.nome} criado com sucesso!",
            success=True
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@app.post("/auth/login", response_model=TokenResponse, tags=["Autenticação"])
async def login_user(
    credentials: UsuarioLogin,
    request: Request,
    db: Session = Depends(get_database_session)
):
    """Login de usuário"""
    # Autenticar usuário
    user = authenticate_user(db, credentials.email, credentials.senha)
    if not user:
        # Registrar tentativa de login falhada
        historico = HistoricoLogin(
            usuario_id=0,  # ID 0 para tentativas falhadas
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            sucesso=False
        )
        db.add(historico)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    # Criar token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    # Atualizar último acesso
    UsuarioService.update_last_access(db, user.id)
    
    # Registrar login bem-sucedido
    historico = HistoricoLogin(
        usuario_id=user.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        sucesso=True
    )
    db.add(historico)
    db.commit()
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UsuarioResponse.from_orm(user)
    )

@app.get("/auth/me", response_model=UsuarioResponse, tags=["Autenticação"])
async def get_current_user_info(current_user: Usuario = Depends(get_current_user)):
    """Obter informações do usuário atual"""
    return UsuarioResponse.from_orm(current_user)

# ================================
# ROTAS DE USUÁRIOS
# ================================

@app.get("/users", response_model=list[UsuarioResponse], tags=["Usuários"])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(require_admin),
    db: Session = Depends(get_database_session)
):
    """Listar usuários (apenas diretores)"""
    users, total = UsuarioService.get_users(db, skip, limit)
    return [UsuarioResponse.from_orm(user) for user in users]

@app.get("/users/{user_id}", response_model=UsuarioResponse, tags=["Usuários"])
async def get_user(
    user_id: int,
    current_user: Usuario = Depends(require_admin),
    db: Session = Depends(get_database_session)
):
    """Obter usuário por ID (apenas diretores)"""
    user = UsuarioService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return UsuarioResponse.from_orm(user)

@app.put("/users/{user_id}", response_model=UsuarioResponse, tags=["Usuários"])
async def update_user(
    user_id: int,
    user_data: UsuarioUpdate,
    current_user: Usuario = Depends(require_admin),
    db: Session = Depends(get_database_session)
):
    """Atualizar usuário (apenas diretores)"""
    user = UsuarioService.update_user(db, user_id, user_data)
    return UsuarioResponse.from_orm(user)

# ================================
# ROTAS DE TURMAS
# ================================

@app.post("/turmas", response_model=TurmaResponse, tags=["Turmas"])
async def create_turma(
    turma_data: TurmaCreate,
    current_user: Usuario = Depends(require_admin_or_coordinator),
    db: Session = Depends(get_database_session)
):
    """Criar nova turma"""
    turma = TurmaService.create_turma(db, turma_data)
    return TurmaResponse.from_orm(turma)

@app.get("/turmas", response_model=list[TurmaResponse], tags=["Turmas"])
async def list_turmas(
    skip: int = 0,
    limit: int = 100,
    ativas_apenas: bool = True,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """Listar turmas"""
    turmas = TurmaService.get_turmas_with_stats(db)
    return turmas

@app.get("/turmas/{turma_id}", response_model=TurmaResponse, tags=["Turmas"])
async def get_turma(
    turma_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """Obter turma por ID"""
    turma = TurmaService.get_turma_by_id(db, turma_id)
    if not turma:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma não encontrada"
        )
    return TurmaResponse.from_orm(turma)

@app.put("/turmas/{turma_id}", response_model=TurmaResponse, tags=["Turmas"])
async def update_turma(
    turma_id: int,
    turma_data: TurmaUpdate,
    current_user: Usuario = Depends(require_admin_or_coordinator),
    db: Session = Depends(get_database_session)
):
    """Atualizar turma"""
    turma = TurmaService.update_turma(db, turma_id, turma_data)
    return TurmaResponse.from_orm(turma)

@app.delete("/turmas/{turma_id}", response_model=MessageResponse, tags=["Turmas"])
async def delete_turma(
    turma_id: int,
    current_user: Usuario = Depends(require_admin),
    db: Session = Depends(get_database_session)
):
    """Excluir turma (apenas diretores)"""
    success = TurmaService.delete_turma(db, turma_id)
    if success:
        return MessageResponse(message="Turma excluída com sucesso")
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Erro ao excluir turma"
    )

# ================================
# ROTAS DE ALUNOS
# ================================

@app.post("/alunos", response_model=AlunoResponse, tags=["Alunos"])
async def create_aluno(
    aluno_data: AlunoCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """Criar novo aluno"""
    aluno = AlunoService.create_aluno(db, aluno_data)
    return AlunoResponse.from_orm(aluno)

@app.get("/alunos", response_model=list[AlunoResponse], tags=["Alunos"])
async def list_alunos(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    turma_id: int = None,
    status: str = None,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """Listar alunos com filtros"""
    alunos = AlunoService.get_alunos_with_turma(db)
    
    # Aplicar filtros
    if search:
        alunos = [a for a in alunos if search.lower() in a.nome.lower() or (a.email and search.lower() in a.email.lower())]
    
    if turma_id:
        alunos = [a for a in alunos if a.turma_id == turma_id]
    
    if status:
        alunos = [a for a in alunos if a.status.value == status]
    
    # Aplicar paginação
    start = skip
    end = skip + limit
    return alunos[start:end]

@app.get("/alunos/{aluno_id}", response_model=AlunoResponse, tags=["Alunos"])
async def get_aluno(
    aluno_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """Obter aluno por ID"""
    aluno = AlunoService.get_aluno_by_id(db, aluno_id)
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    return AlunoResponse.from_orm(aluno)

@app.put("/alunos/{aluno_id}", response_model=AlunoResponse, tags=["Alunos"])
async def update_aluno(
    aluno_id: int,
    aluno_data: AlunoUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """Atualizar aluno"""
    aluno = AlunoService.update_aluno(db, aluno_id, aluno_data)
    return AlunoResponse.from_orm(aluno)

@app.delete("/alunos/{aluno_id}", response_model=MessageResponse, tags=["Alunos"])
async def delete_aluno(
    aluno_id: int,
    current_user: Usuario = Depends(require_admin_or_coordinator),
    db: Session = Depends(get_database_session)
):
    """Inativar aluno"""
    success = AlunoService.delete_aluno(db, aluno_id)
    if success:
        return MessageResponse(message="Aluno inativado com sucesso")
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Erro ao inativar aluno"
    )

# ================================
# ROTAS DE ESTATÍSTICAS
# ================================

@app.get("/statistics", response_model=StatisticsResponse, tags=["Estatísticas"])
async def get_statistics(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """Obter estatísticas do sistema"""
    stats = StatisticsService.get_dashboard_stats(db)
    return StatisticsResponse(**stats)

# ================================
# ROTA RAIZ
# ================================

@app.get("/", tags=["Sistema"])
async def root():
    """Rota raiz da API"""
    return {
        "message": "🎓 Sistema de Gestão Escolar API",
        "version": "1.0.0",
        "status": "✅ Online",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "database": "connected"
    }

# ================================
# HANDLER DE ERROS
# ================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler customizado para exceções HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler geral para exceções"""
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Erro interno do servidor",
            "status_code": 500
        }
    )

# ================================
# EXECUTAR APLICAÇÃO
# ================================

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
