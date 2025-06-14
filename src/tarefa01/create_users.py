import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection

def create_users():
    """Cria os usuários necessários para os testes de controle de acesso"""
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    # Usar nomes em minúscula para evitar problemas de case-sensitivity
    users = ['usr_a', 'usr_b', 'usr_c', 'usr_d', 'usr_e']
    passwords = ['usr_a123', 'usr_b123', 'usr_c123', 'usr_d123', 'usr_e123']
    
    try:
        for i, user in enumerate(users):
            # Remover usuário se existir
            db.execute_query(f"DROP USER IF EXISTS {user};")
            time.sleep(0.2)
            
            # Criar usuário com permissão de LOGIN
            db.execute_query(f"CREATE USER {user} WITH PASSWORD '{passwords[i]}' LOGIN;")
            print(f"   Usuário {user} criado com sucesso!")
            time.sleep(0.5)
        
        return True
        
    except Exception as e:
        print(f"Erro ao criar usuários: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    create_users()
