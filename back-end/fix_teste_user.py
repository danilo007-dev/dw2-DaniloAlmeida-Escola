#!/usr/bin/env python3
"""
Script para corrigir o cargo do usuário Teste
"""

from database import SessionLocal
from models import Usuario, CargoEnum
from sqlalchemy import text

def fix_teste_user():
    db = SessionLocal()
    try:
        print("🔧 Corrigindo cargo do usuário Teste...")
        
        # Buscar usuário Teste
        user = db.query(Usuario).filter(
            Usuario.nome.like('%Teste%')
        ).first()
        
        if user:
            print(f"📋 Usuário encontrado: {user.nome} ({user.email})")
            print(f"🔄 Cargo atual: {user.cargo}")
            
            # Atualizar cargo para diretor
            user.cargo = CargoEnum.diretor
            db.commit()
            
            print(f"✅ Cargo atualizado para: {user.cargo}")
        else:
            print("❌ Usuário Teste não encontrado")
            
        # Verificar outros usuários com problemas
        print("\n📋 Verificando todos os usuários:")
        users = db.query(Usuario).all()
        for u in users:
            print(f"ID: {u.id}, Nome: {u.nome}, Email: {u.email}, Cargo: {u.cargo}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_teste_user()
