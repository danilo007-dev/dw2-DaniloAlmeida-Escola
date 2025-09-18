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
            # ENSINO FUNDAMENTAL - ANOS INICIAIS (1º ao 5º ano)
            # 1º ANO
            {
                "nome": "1º ANO A",
                "descricao": "Primeiro ano do ensino fundamental - Turma A",
                "capacidade": 25,
                "ano_letivo": "2024",
                "periodo": "Matutino"
            },
            {
                "nome": "1º ANO B",
                "descricao": "Primeiro ano do ensino fundamental - Turma B",
                "capacidade": 25,
                "ano_letivo": "2024",
                "periodo": "Vespertino"
            },
            
            # 2º ANO
            {
                "nome": "2º ANO A",
                "descricao": "Segunda série do ensino fundamental - Turma A", 
                "capacidade": 28,
                "ano_letivo": "2024",
                "periodo": "Matutino"
            },
            {
                "nome": "2º ANO B",
                "descricao": "Segunda série do ensino fundamental - Turma B",
                "capacidade": 30,
                "ano_letivo": "2024",
                "periodo": "Vespertino"
            },
            
            # 3º ANO
            {
                "nome": "3º ANO A",
                "descricao": "Terceira série do ensino fundamental - Turma A",
                "capacidade": 26,
                "ano_letivo": "2024",
                "periodo": "Matutino"
            },
            {
                "nome": "3º ANO B",
                "descricao": "Terceira série do ensino fundamental - Turma B",
                "capacidade": 28,
                "ano_letivo": "2024",
                "periodo": "Vespertino"
            },
            
            # 4º ANO
            {
                "nome": "4º ANO A",
                "descricao": "Quarta série do ensino fundamental - Turma A",
                "capacidade": 24,
                "ano_letivo": "2024",
                "periodo": "Matutino"
            },
            {
                "nome": "4º ANO B",
                "descricao": "Quarta série do ensino fundamental - Turma B",
                "capacidade": 26,
                "ano_letivo": "2024",
                "periodo": "Vespertino"
            },
            
            # 5º ANO
            {
                "nome": "5º ANO A",
                "descricao": "Quinta série do ensino fundamental - Turma A",
                "capacidade": 30,
                "ano_letivo": "2024",
                "periodo": "Matutino"
            },
            {
                "nome": "5º ANO B",
                "descricao": "Quinta série do ensino fundamental - Turma B",
                "capacidade": 28,
                "ano_letivo": "2024",
                "periodo": "Vespertino"
            },
            
            # ENSINO FUNDAMENTAL - ANOS FINAIS (6º ao 9º ano)
            # 6º ANO
            {
                "nome": "6º ANO A",
                "descricao": "Sexta série do ensino fundamental - Turma A",
                "capacidade": 32,
                "ano_letivo": "2024",
                "periodo": "Matutino"
            },
            {
                "nome": "6º ANO B",
                "descricao": "Sexta série do ensino fundamental - Turma B",
                "capacidade": 30,
                "ano_letivo": "2024",
                "periodo": "Vespertino"
            },
            
            # 7º ANO
            {
                "nome": "7º ANO A",
                "descricao": "Sétima série do ensino fundamental - Turma A",
                "capacidade": 35,
                "ano_letivo": "2024",
                "periodo": "Matutino"
            },
            {
                "nome": "7º ANO B",
                "descricao": "Sétima série do ensino fundamental - Turma B",
                "capacidade": 33,
                "ano_letivo": "2024",
                "periodo": "Vespertino"
            },
            
            # 8º ANO
            {
                "nome": "8º ANO A",
                "descricao": "Oitava série do ensino fundamental - Turma A",
                "capacidade": 30,
                "ano_letivo": "2024",
                "periodo": "Matutino"
            },
            {
                "nome": "8º ANO B",
                "descricao": "Oitava série do ensino fundamental - Turma B",
                "capacidade": 32,
                "ano_letivo": "2024",
                "periodo": "Vespertino"
            },
            
            # 9º ANO
            {
                "nome": "9º ANO A",
                "descricao": "Nona série do ensino fundamental - Turma A",
                "capacidade": 28,
                "ano_letivo": "2024",
                "periodo": "Matutino"
            },
            {
                "nome": "9º ANO B",
                "descricao": "Nona série do ensino fundamental - Turma B",
                "capacidade": 30,
                "ano_letivo": "2024",
                "periodo": "Vespertino"
            },
            
            # ENSINO MÉDIO
            # 1º ANO MÉDIO
            {
                "nome": "1º MÉDIO A",
                "descricao": "Primeiro ano do ensino médio - Turma A",
                "capacidade": 35,
                "ano_letivo": "2024",
                "periodo": "Matutino"
            },
            {
                "nome": "1º MÉDIO B",
                "descricao": "Primeiro ano do ensino médio - Turma B",
                "capacidade": 40,
                "ano_letivo": "2024",
                "periodo": "Noturno"
            },
            
            # 2º ANO MÉDIO
            {
                "nome": "2º MÉDIO A",
                "descricao": "Segunda série do ensino médio - Turma A",
                "capacidade": 38,
                "ano_letivo": "2024",
                "periodo": "Matutino"
            },
            {
                "nome": "2º MÉDIO B",
                "descricao": "Segunda série do ensino médio - Turma B",
                "capacidade": 35,
                "ano_letivo": "2024",
                "periodo": "Noturno"
            },
            
            # 3º ANO MÉDIO
            {
                "nome": "3º MÉDIO A",
                "descricao": "Terceira série do ensino médio - Turma A",
                "capacidade": 32,
                "ano_letivo": "2024",
                "periodo": "Matutino"
            },
            {
                "nome": "3º MÉDIO B",
                "descricao": "Terceira série do ensino médio - Turma B",
                "capacidade": 30,
                "ano_letivo": "2024",
                "periodo": "Noturno"
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
        
        # Criar alunos variados
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
                "turma_id": turmas[4].id,  # 3º ANO A
                "observacoes": "Aluna exemplar, sempre pontual"
            },
            {
                "nome": "Bruno Costa Oliveira",
                "cpf": "123.456.789-02",
                "data_nascimento": date(2009, 11, 22),
                "email": "bruno.costa@email.com",
                "telefone": "(11) 99999-2345",
                "endereco": "Av. Principal, 456 - Jardim",
                "nome_responsavel": "João Costa Oliveira",
                "telefone_responsavel": "(11) 99999-6789",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 5),
                "turma_id": turmas[5].id,  # 3º ANO B
                "observacoes": "Bom desempenho em matemática"
            },
            {
                "nome": "Carla Fernanda Lima",
                "cpf": "123.456.789-03",
                "data_nascimento": date(2011, 7, 8),
                "email": "carla.lima@email.com",
                "telefone": "(11) 99999-3456",
                "endereco": "Rua do Sol, 789 - Vila Nova",
                "nome_responsavel": "José Lima",
                "telefone_responsavel": "(11) 99999-7890",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 8),
                "turma_id": turmas[2].id,  # 2º ANO A
                "observacoes": "Muito criativa nas aulas de arte"
            },
            {
                "nome": "Diego Santos Pereira",
                "cpf": "123.456.789-04",
                "data_nascimento": date(2010, 1, 30),
                "email": "diego.pereira@email.com",
                "telefone": "(11) 99999-4567",
                "endereco": "Rua Nova, 321 - Bairro Alto",
                "nome_responsavel": "Rosa Santos Pereira",
                "telefone_responsavel": "(11) 99999-8901",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 10),
                "turma_id": turmas[4].id,  # 3º ANO A
                "observacoes": "Excelente em educação física"
            },
            {
                "nome": "Eduarda Martins Rocha",
                "cpf": "123.456.789-05",
                "data_nascimento": date(2011, 5, 12),
                "email": "eduarda.rocha@email.com",
                "telefone": "(11) 99999-5678",
                "endereco": "Av. Central, 654 - Centro",
                "nome_responsavel": "Carlos Martins",
                "telefone_responsavel": "(11) 99999-9012",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 12),
                "turma_id": turmas[3].id,  # 2º ANO B
                "observacoes": "Ótima leitura e interpretação"
            },
            {
                "nome": "Felipe Alves Souza",
                "cpf": "123.456.789-06",
                "data_nascimento": date(2011, 9, 25),
                "email": "felipe.souza@email.com",
                "telefone": "(11) 99999-6789",
                "endereco": "Rua da Paz, 987 - Jardim",
                "nome_responsavel": "Marina Alves",
                "telefone_responsavel": "(11) 99999-0123",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 15),
                "turma_id": turmas[2].id,  # 2º ANO A
                "observacoes": "Precisa melhorar a concentração"
            },
            {
                "nome": "Gabriela Torres Silva",
                "cpf": "123.456.789-07",
                "data_nascimento": date(2009, 12, 3),
                "email": "gabriela.torres@email.com",
                "telefone": "(11) 99999-7890",
                "endereco": "Rua Verde, 147 - Vila Sul",
                "nome_responsavel": "Roberto Torres",
                "telefone_responsavel": "(11) 99999-1357",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 18),
                "turma_id": turmas[6].id,  # 4º ANO A
                "observacoes": "Líder natural da turma"
            },
            {
                "nome": "Henrique Barbosa Dias",
                "cpf": "123.456.789-08",
                "data_nascimento": date(2012, 4, 17),
                "email": None,
                "telefone": "(11) 99999-8901",
                "endereco": "Av. das Águas, 258 - Centro",
                "nome_responsavel": "Lucia Barbosa",
                "telefone_responsavel": "(11) 99999-2468",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 20),
                "turma_id": turmas[0].id,  # 1º ANO A
                "observacoes": None
            },
            {
                "nome": "Isabela Nascimento Costa",
                "cpf": "123.456.789-09",
                "data_nascimento": date(2005, 8, 14),
                "email": "isabela.costa@email.com",
                "telefone": "(11) 99999-9012",
                "endereco": "Rua Azul, 369 - Bairro Novo",
                "nome_responsavel": "Fernando Costa",
                "telefone_responsavel": "(11) 99999-3579",
                "status": StatusAlunoEnum.inativo,
                "data_matricula": date(2024, 2, 22),
                "turma_id": turmas[18].id,  # 1º MÉDIO A
                "observacoes": "Transferida para outra escola"
            },
            {
                "nome": "João Pedro Moreira Lima",
                "cpf": "123.456.789-10",
                "data_nascimento": date(2006, 10, 9),
                "email": "joao.lima@email.com",
                "telefone": "(11) 99999-0123",
                "endereco": "Rua da Esperança, 741 - Vila Norte",
                "nome_responsavel": "Sandra Moreira",
                "telefone_responsavel": "(11) 99999-4680",
                "status": StatusAlunoEnum.ativo,
                "data_matricula": date(2024, 2, 25),
                "turma_id": turmas[22].id,  # 3º MÉDIO A
                "observacoes": "Excelente em química e física"
            }
        ]
        
        for aluno_data in alunos_data:
            aluno = Aluno(**aluno_data)
            db.add(aluno)
        
        db.commit()
        print("✅ Alunos criados!")
        
        print("🎉 Dados iniciais criados com sucesso!")
        print("\n📋 Resumo:")
        print(f"   👥 {len([admin_user, coord_user, sec_user, prof_user])} usuários criados")
        print(f"   📚 {len(turmas_data)} turmas criadas")
        print(f"   🎓 {len(alunos_data)} alunos criados")
        
        print("\n🔐 Credenciais de acesso:")
        print("   📧 admin@escola.com | 🔑 123456 (Diretor)")
        print("   📧 maria@escola.com | 🔑 123456 (Coordenador)")
        print("   📧 ana@escola.com   | 🔑 123456 (Secretário)")
        print("   📧 joao@escola.com  | 🔑 123456 (Professor)")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_data()