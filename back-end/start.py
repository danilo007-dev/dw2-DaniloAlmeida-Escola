# start.py
# Script para inicializar o sistema completo
import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    try:
        import fastapi
        import sqlalchemy
        import uvicorn
        import pydantic
        import python_jose
        import passlib
        print("✅ Todas as dependências estão instaladas!")
        return True
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        return False

def initialize_database():
    """Inicializa o banco de dados e popula com dados iniciais"""
    print("\n🗄️ Inicializando banco de dados...")
    try:
        from seed import create_initial_data
        create_initial_data()
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        return False

def start_server():
    """Inicia o servidor FastAPI"""
    print("\n🚀 Iniciando servidor...")
    try:
        os.system("uvicorn app:app --host 0.0.0.0 --port 8000 --reload")
    except KeyboardInterrupt:
        print("\n⏹️ Servidor parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")

def main():
    """Função principal"""
    print("🏫 Sistema de Gestão Escolar")
    print("=" * 40)
    
    # Verificar dependências
    if not check_dependencies():
        sys.exit(1)
    
    # Inicializar banco
    if not initialize_database():
        print("⚠️ Continuando mesmo com erro no banco...")
    
    # Iniciar servidor
    start_server()

if __name__ == "__main__":
    main()
