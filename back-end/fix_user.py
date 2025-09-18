#!/usr/bin/env python3
# Script temporário para corrigir cargo do usuário

import sqlite3
import os

def fix_user_role():
    db_path = 'escola.db'
    
    if not os.path.exists(db_path):
        print(f"Banco de dados não encontrado: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar usuários atuais
        print("=== VERIFICANDO USUÁRIOS ===")
        cursor.execute('SELECT id, nome, email, cargo FROM usuarios ORDER BY id')
        users = cursor.fetchall()
        
        for user in users:
            print(f"ID: {user[0]} | Nome: {user[1]} | Email: {user[2]} | Cargo: {user[3]}")
        
        # Encontrar e atualizar usuário Danilo
        cursor.execute('SELECT id, nome, cargo FROM usuarios WHERE nome LIKE "%Danilo%"')
        danilo_users = cursor.fetchall()
        
        if danilo_users:
            print(f"\n=== USUÁRIOS DANILO ENCONTRADOS: {len(danilo_users)} ===")
            
            for user in danilo_users:
                user_id, nome, cargo_atual = user
                print(f"ID: {user_id} | Nome: {nome} | Cargo atual: {cargo_atual}")
                
                # Atualizar para diretor
                cursor.execute('UPDATE usuarios SET cargo = ? WHERE id = ?', ('diretor', user_id))
                print(f"Cargo do usuário {nome} atualizado para 'diretor'")
            
            conn.commit()
            print("\n✅ Atualizações salvas com sucesso!")
            
            # Verificar após atualização
            print("\n=== VERIFICAÇÃO APÓS ATUALIZAÇÃO ===")
            cursor.execute('SELECT id, nome, email, cargo FROM usuarios ORDER BY id')
            updated_users = cursor.fetchall()
            
            for user in updated_users:
                print(f"ID: {user[0]} | Nome: {user[1]} | Email: {user[2]} | Cargo: {user[3]}")
                
        else:
            print("\n❌ Nenhum usuário com nome 'Danilo' encontrado")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    fix_user_role()
