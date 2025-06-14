import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection

def cleanup_vendasdb():
    """Remove roles e revoga privilégios do VENDASDB"""
    print("Iniciando limpeza do VENDASDB...")
    
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        print("Erro ao conectar para limpeza")
        return False
    
    try:
        # Revogar roles dos usuários
        print("Revogando roles dos usuários...")
        users = ['usr_a', 'usr_b', 'usr_c', 'usr_d', 'usr_e']
        roles = ['role_adm', 'role_gerente', 'role_atendente']
        
        for user in users:
            for role in roles:
                try:
                    db.execute_query(f"REVOKE {role} FROM {user};")
                    time.sleep(0.1)
                except Exception:
                    pass 
        
        # Revogar privilégios das roles nas tabelas
        print("Revogando privilégios das roles...")
        tables = ['customer', 'supplier', 'product', 'orders', 'orderitem']
        
        for role in roles:
            # Revogar privilégios do schema
            try:
                db.execute_query(f"REVOKE ALL ON SCHEMA vendasdb FROM {role};")
                time.sleep(0.1)
            except Exception:
                pass
            
            # Revogar privilégios das tabelas
            for table in tables:
                try:
                    db.execute_query(f"REVOKE ALL PRIVILEGES ON vendasdb.{table} FROM {role};")
                    time.sleep(0.1)
                except Exception:
                    pass  
        
        time.sleep(1)
        
        # Remover roles
        print("Removendo roles...")
        for role in roles:
            try:
                db.execute_query(f"DROP ROLE IF EXISTS {role};")
                print(f"   Role {role} removida")
                time.sleep(0.2)
            except Exception as e:
                print(f"   Erro ao remover role {role}: {e}")
        
        print("Limpeza do VENDASDB concluída!")
        return True
        
    except Exception as e:
        print(f"Erro durante limpeza: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    cleanup_vendasdb()
