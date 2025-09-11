# seed.py
# seed.py
# Script para popular o banco de dados com dados iniciais
from sqlalchemy.orm import Session
from database import SessionLocal, init_database
from models import Usuario, Turma, Aluno, StatusAlunoEnum, CargoEnum
from auth import get_password_hash
from datetime import date, datetime

def create_initial_data():
    """Cria dados iniciais no banco de dados"""
    print("🌱 Criando dados iniciais...")
    
    # Inicializar banco
    init_database()
    
    # Criar sessão
    db = SessionLocal()
    
    try:
        # Verificar se já existem dados
        existing_users = db.query(Usuario).count()
        if existing_users > 0:
            print("📋 Dados já existem no banco. Pulando criação inicial.")
            return
        
        # Criar usuários iniciais
        print("👥 Criando usuários...")
        
        # Diretor
        admin_user = Usuario(
            nome="Admin Sistema",
            email="admin@escola.com",
            senha_hash=get_password_hash("123456"),
            cargo=CargoEnum.diretor,
            ativo=True
        )
        db.add(admin_user)
        
        # Coordenadora
        coord_user = Usuario(
            nome="Maria Santos Silva",
            email="maria@escola.com",
            senha_hash=get_password_hash("123456"),
            cargo=CargoEnum.coordenador,
            ativo=True
        )
        db.add(coord_user)
        
        # Secretária
        sec_user = Usuario(
            nome="Ana Paula Costa",
            email="ana@escola.com",
            senha_hash=get_password_hash("123456"),
            cargo=CargoEnum.secretario,
            ativo=True
        )
        db.add(sec_user)
        
        # Professor
        prof_user = Usuario(
            nome="João Carlos Oliveira",
            email="joao@escola.com",
            senha_hash=get_password_hash("123456"),
            cargo=CargoEnum.professor,
            ativo=True
        )
        db.add(prof_user)
        
        db.commit()
        print("✅ Usuários criados!")
        
        # Criar turmas
        print("📚 Criando turmas...")
        
        turmas_data = [
            {
                "nome": "1º ANO A",
                "descricao": "Primeira série do ensino fundamental - Turma A",
                "capacidade": 25,
                "ano_letivo": "2024",
                "periodo": "Manhã"
            },
            {
                "nome": "2º ANO A",
                "descricao": "Segunda série do ensino fundamental - Turma A", 
                "capacidade": 28,
                "ano_letivo": "2024",
                "periodo": "Manhã"
            },
            {
                "nome": "2º ANO B",
                "descricao": "Segunda série do ensino fundamental - Turma B",
                "capacidade": 30,
                "ano_letivo": "2024",
                "periodo": "Tarde"
            },
            {
                "nome": "3º ANO A",
                "descricao": "Terceira série do ensino fundamental - Turma A",
                "capacidade": 26,
                "ano_letivo": "2024",
                "periodo": "Manhã"
            },
            {
                "nome": "3º ANO B",
                "descricao": "Terceira série do ensino fundamental - Turma B",
                "capacidade": 28,
                "ano_letivo": "2024",
                "periodo": "Tarde"
            },
            {
                "nome": "4º ANO A",
                "descricao": "Quarta série do ensino fundamental - Turma A",
                "capacidade": 24,
                "ano_letivo": "2024",
                "periodo": "Manhã"
            }
        ]
        
        turmas = []
        for turma_data in turmas_data:
            turma = Turma(**turma_data)
            db.add(turma)
            turmas.append(turma)
        
        db.commit()
        print("✅ Turmas criadas!")
        
        # Refresh para obter IDs
        for turma in turmas:
            db.refresh(turma)
        
        # Criar alunos
        print("👥 Criando alunos...")
        
        alunos_data = [
            {
                "nome": "Ana Clara Silva Santos",
                "cpf": "123.456.789-01",
                "data_nascimento": date(2010, 3, 15),
                "email": "ana.silva@email.com",
                "telefone": "(11) 99999-1234",
                "endereco": "Rua das Flores, 123 - Centro",
                "nome_responsavel": "Maria Silva Santos",
                "telefone_responsavel": "(11) 99999-5678",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 1),
                "turma_id": turmas[3].id,  # 3º ANO A
                "observacoes": "Aluna exemplar, sempre pontual"
            },
            {
                "nome": "Bruno Costa Oliveira",
                "cpf": "123.456.789-02",
                "data_nascimento": date(2009, 11, 22),
                "email": "bruno.costa@email.com",
                "telefone": "(11) 99999-2345",
                "endereco": "Av. Principal, 456 - Jardim",
                "nome_responsavel": "Carlos Costa Oliveira",
                "telefone_responsavel": "(11) 99999-6789",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 1),
                "turma_id": turmas[4].id,  # 3º ANO B
                "observacoes": "Bom rendimento em matemática"
            },
            {
                "nome": "Carla Fernanda Lima",
                "cpf": "123.456.789-03",
                "data_nascimento": date(2011, 7, 8),
                "email": "carla.lima@email.com",
                "telefone": "(11) 99999-3456",
                "endereco": "Rua da Paz, 789 - Vila Nova",
                "nome_responsavel": "Fernanda Lima",
                "telefone_responsavel": "(11) 99999-7890",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 1),
                "turma_id": turmas[1].id,  # 2º ANO A
                "observacoes": "Muito criativa nas atividades de arte"
            },
            {
                "nome": "Diego Santos Pereira",
                "cpf": "123.456.789-04",
                "data_nascimento": date(2010, 12, 3),
                "email": "diego.santos@email.com",
                "telefone": "(11) 99999-4567",
                "endereco": "Rua do Sol, 321 - Bairro Alto",
                "nome_responsavel": "Sandra Santos Pereira",
                "telefone_responsavel": "(11) 99999-8901",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 1),
                "turma_id": turmas[3].id,  # 3º ANO A
                "observacoes": "Gosta muito de educação física"
            },
            {
                "nome": "Elena Rodriguez Gonçalves",
                "cpf": "123.456.789-05",
                "data_nascimento": date(2012, 5, 17),
                "email": "elena.rodriguez@email.com",
                "telefone": "(11) 99999-5678",
                "endereco": "Rua das Palmeiras, 654 - Centro",
                "nome_responsavel": "Carmen Rodriguez",
                "telefone_responsavel": "(11) 99999-9012",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 1),
                "turma_id": turmas[2].id,  # 2º ANO B
                "observacoes": "Bilíngue, fala espanhol fluentemente"
            },
            {
                "nome": "Felipe Almeida Castro",
                "cpf": "123.456.789-06",
                "data_nascimento": date(2011, 9, 25),
                "email": "felipe.almeida@email.com",
                "telefone": "(11) 99999-6789",
                "endereco": "Av. das Nações, 987 - Jardim Europa",
                "nome_responsavel": "Roberto Almeida Castro",
                "telefone_responsavel": "(11) 99999-0123",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 1),
                "turma_id": turmas[1].id,  # 2º ANO A
                "observacoes": "Excelente em leitura"
            },
            {
                "nome": "Gabriela Ferreira Rocha",
                "cpf": "123.456.789-07",
                "data_nascimento": date(2010, 1, 12),
                "email": "gabriela.ferreira@email.com",
                "telefone": "(11) 99999-7890",
                "endereco": "Rua Nova, 147 - Vila Esperança",
                "nome_responsavel": "Luciana Ferreira",
                "telefone_responsavel": "(11) 99999-1234",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 1),
                "turma_id": turmas[5].id,  # 4º ANO A
                "observacoes": "Líder natural, sempre ajuda os colegas"
            },
            {
                "nome": "Henrique Barbosa Martins",
                "cpf": "123.456.789-08",
                "data_nascimento": date(2012, 8, 30),
                "data_matricula": date(2024, 2, 1),
                "status": StatusAlunoEnum.ativo,
                "turma_id": turmas[0].id,  # 1º ANO A
                "nome_responsavel": "Ana Barbosa Martins",
                "telefone_responsavel": "(11) 99999-2345",
                "observacoes": "Primeiro ano, adaptação muito boa"
            },
            {
                "nome": "Isabella Campos Nunes",
                "cpf": "123.456.789-09",
                "data_nascimento": date(2011, 4, 18),
                "email": "isabella.campos@email.com",
                "telefone": "(11) 99999-8901",
                "endereco": "Rua Verde, 258 - Parque das Árvores",
                "nome_responsavel": "Patricia Campos",
                "telefone_responsavel": "(11) 99999-3456",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 1),
                "turma_id": turmas[2].id,  # 2º ANO B
                "observacoes": "Muito participativa em sala"
            },
            {
                "nome": "João Pedro Sousa Lima",
                "cpf": "123.456.789-10",
                "data_nascimento": date(2010, 6, 14),
                "status": StatusAlunoEnum.inativo,
                "data_matricula": date(2024, 2, 1),
                "turma_id": turmas[3].id,  # 3º ANO A
                "nome_responsavel": "Marcos Sousa Lima",
                "telefone_responsavel": "(11) 99999-4567",
                "observacoes": "Transferido para outra escola em setembro"
            }
        ]
        
        for aluno_data in alunos_data:
            aluno = Aluno(**aluno_data)
            db.add(aluno)
        
        db.commit()
        print("✅ Alunos criados!")
        
        print("\n🎉 Dados iniciais criados com sucesso!")
        print("\n📋 Usuários de teste:")
        print("👤 admin@escola.com / 123456 (Diretor)")
        print("👤 maria@escola.com / 123456 (Coordenadora)")
        print("👤 ana@escola.com / 123456 (Secretária)")
        print("👤 joao@escola.com / 123456 (Professor)")
        
        print("\n📊 Estatísticas:")
        total_usuarios = db.query(Usuario).count()
        total_turmas = db.query(Turma).count()
        total_alunos = db.query(Aluno).count()
        alunos_ativos = db.query(Aluno).filter(Aluno.status == StatusAlunoEnum.ativo).count()
        
        print(f"👥 {total_usuarios} usuários")
        print(f"📚 {total_turmas} turmas")
        print(f"🎓 {total_alunos} alunos ({alunos_ativos} ativos)")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados iniciais: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_data()
