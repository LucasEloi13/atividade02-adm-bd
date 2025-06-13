import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection

def cleanup_all():
    """Remove todos os usuários, visões e privilégios criados nos testes"""
    print("Iniciando limpeza do ambiente...")
    time.sleep(1)
    
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        print("Erro ao conectar para limpeza")
        return False
    
    users = ['usr_a', 'usr_b', 'usr_c', 'usr_d', 'usr_e']
    views = [
        'vw_funcionario_usr_b',
        'vw_departamento_usr_b', 
        'vw_funcionario_usr_c',
        'vw_projeto_usr_c',
        'vw_funcionario_usr_e'
    ]
    
    try:
        # Remover visões
        print("Removendo visões...")
        for view in views:
            try:
                db.execute_query(f"DROP VIEW IF EXISTS {view} CASCADE;")
                print(f"   Visão {view} removida")
                time.sleep(0.2)
            except Exception as e:
                print(f"   Erro ao remover visão {view}: {e}")
        
        time.sleep(1)
        
        # Revogar todos os privilégios antes de remover usuários
        print("Revogando privilégios...")
        tables = ['FUNCIONARIO', 'DEPARTAMENTO', 'LOCALIZACAO_DEP', 'PROJETO', 'TRABALHA_EM', 'DEPENDENTE']
        
        for user in users:
            for table in tables:
                try:
                    db.execute_query(f"REVOKE ALL PRIVILEGES ON {table} FROM {user};")
                    time.sleep(0.1)
                except Exception:
                    pass  # Ignora erros (usuário pode não ter privilégios)
        
        time.sleep(1)
        
        # Remover usuários
        print("Removendo usuários...")
        for user in users:
            try:
                # Terminar conexões ativas do usuário
                db.execute_query(f"""
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity 
                    WHERE usename = '{user}';
                """)
                
                # Remover usuário
                db.execute_query(f"DROP USER IF EXISTS {user};")
                print(f"   Usuário {user} removido")
                time.sleep(0.3)
            except Exception as e:
                print(f"   Erro ao remover usuário {user}: {e}")
        
        time.sleep(1)
        print("Limpeza concluída com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro durante limpeza: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    cleanup_all()
