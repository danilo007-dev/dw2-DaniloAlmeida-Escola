#!/usr/bin/env python3
import requests
import json

# URL base da API
BASE_URL = "http://localhost:8000"

def test_login():
    """Testa o login e retorna o token"""
    print("🔐 Testando login...")
    
    data = {
        "email": "admin@escola.com",
        "senha": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        print(f"Status login: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login realizado com sucesso!")
            return result.get("access_token"), result.get("token_type", "Bearer")
        else:
            print(f"❌ Erro no login: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None, None

def test_turmas(token, token_type):
    """Testa o endpoint de turmas"""
    print("\n📚 Testando endpoint de turmas...")
    
    headers = {
        "Authorization": f"{token_type} {token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/turmas", headers=headers)
        print(f"Status turmas: {response.status_code}")
        
        if response.status_code == 200:
            turmas = response.json()
            print(f"✅ Turmas encontradas: {len(turmas)}")
            for i, turma in enumerate(turmas[:3]):
                print(f"  {i+1}. {turma.get('nome')} - {turma.get('periodo')}")
            return turmas
        else:
            print(f"❌ Erro ao buscar turmas: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return []

def test_alunos(token, token_type):
    """Testa o endpoint de alunos"""
    print("\n🎓 Testando endpoint de alunos...")
    
    headers = {
        "Authorization": f"{token_type} {token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/alunos", headers=headers)
        print(f"Status alunos: {response.status_code}")
        
        if response.status_code == 200:
            alunos = response.json()
            print(f"✅ Alunos encontrados: {len(alunos)}")
            for i, aluno in enumerate(alunos[:3]):
                print(f"  {i+1}. {aluno.get('nome')} - {aluno.get('turma_nome', 'Sem turma')}")
            return alunos
        else:
            print(f"❌ Erro ao buscar alunos: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return []

if __name__ == "__main__":
    print("🧪 Testando API do Sistema de Gestão Escolar")
    print("=" * 50)
    
    # Teste de login
    token, token_type = test_login()
    
    if token:
        # Teste de turmas
        turmas = test_turmas(token, token_type)
        
        # Teste de alunos
        alunos = test_alunos(token, token_type)
        
        print("\n📊 Resumo dos testes:")
        print(f"✅ Login: OK")
        print(f"✅ Turmas: {len(turmas)} encontradas")
        print(f"✅ Alunos: {len(alunos)} encontrados")
    else:
        print("\n❌ Não foi possível realizar os testes devido a falha no login")