#!/usr/bin/env python3
# reset_db.py
# Script para resetar o banco de dados e recriar todos os dados

import os
import sys
from database import init_database, SessionLocal
from models import Usuario, Turma, Aluno

def reset_database():
    """Remove todas as tabelas e recria com dados iniciais"""
    print("🗑️ Resetando banco de dados...")
    
    # Remover arquivo do banco se existir
    db_file = "escola.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        print("✅ Arquivo do banco removido")
    
    # Recriar banco
    print("🔄 Recriando banco de dados...")
    init_database()
    
    # Executar seed
    print("🌱 Executando script de seed...")
    from seed import create_initial_data
    create_initial_data()
    
    print("✅ Banco de dados resetado com sucesso!")

if __name__ == "__main__":
    reset_database()