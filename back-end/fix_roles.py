#!/usr/bin/env python3
# Script para corrigir cargos dos usuários no banco

import sqlite3
import os

def fix_user_roles():
    db_path = 'escola.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("=== USUÁRIOS ANTES DA CORREÇÃO ===")
        cursor.execute('SELECT id, nome, email, cargo FROM usuarios ORDER BY id')
        users = cursor.fetchall()
        
        for user in users:
            print(f"ID: {user[0]} | Nome: {user[1]} | Email: {user[2]} | Cargo: {user[3]}")
        
        # Corrigir usuários específicos
        corrections = [
            # Usuários que deveriam ser diretores
            ("admin@escola.com", "diretor"),
            # Qualquer usuário com nome contendo "Danilo" deveria ser diretor
        ]
        
        # Atualizar usuários por email
        for email, new_cargo in corrections:
            cursor.execute('UPDATE usuarios SET cargo = ? WHERE email = ?', (new_cargo, email))
            print(f"✅ Usuário {email} atualizado para {new_cargo}")
        
        # Atualizar usuários com nome contendo "Danilo"
        cursor.execute('UPDATE usuarios SET cargo = ? WHERE nome LIKE ?', ('diretor', '%Danilo%'))
        affected_rows = cursor.rowcount
        print(f"✅ {affected_rows} usuário(s) com nome 'Danilo' atualizado(s) para diretor")
        
        conn.commit()
        
        print("\n=== USUÁRIOS APÓS CORREÇÃO ===")
        cursor.execute('SELECT id, nome, email, cargo FROM usuarios ORDER BY id')
        updated_users = cursor.fetchall()
        
        for user in updated_users:
            print(f"ID: {user[0]} | Nome: {user[1]} | Email: {user[2]} | Cargo: {user[3]}")
        
        print("\n✅ Correções aplicadas com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    fix_user_roles()
