import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection

def create_roles():
    """Cria as roles para o sistema VENDASDB"""
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    try:
        print("Criando roles...")
        
        # Remover roles se existirem
        roles = ['role_adm', 'role_gerente', 'role_atendente']
        for role in roles:
            db.execute_query(f"DROP ROLE IF EXISTS {role};")
            time.sleep(0.2)
        
        # 1. Criar role_adm - Acesso total
        print("   Criando role_adm...")
        db.execute_query("CREATE ROLE role_adm;")
        
        # Conceder uso do schema
        db.execute_query("GRANT USAGE ON SCHEMA vendasdb TO role_adm;")
        
        # Privilégios completos em todas as tabelas
        tables = ['customer', 'supplier', 'product', 'orders', 'orderitem']
        for table in tables:
            db.execute_query(f"GRANT ALL PRIVILEGES ON vendasdb.{table} TO role_adm;")
        time.sleep(0.5)
        
        # 2. Criar role_gerente - Acesso a fornecedores, produtos e pedidos
        print("   Criando role_gerente...")
        db.execute_query("CREATE ROLE role_gerente;")
        
        # Conceder uso do schema
        db.execute_query("GRANT USAGE ON SCHEMA vendasdb TO role_gerente;")
        
        # Privilégios de leitura e escrita em supplier, product, orders, orderitem
        gerente_tables = ['supplier', 'product', 'orders', 'orderitem']
        for table in gerente_tables:
            db.execute_query(f"GRANT SELECT, INSERT, UPDATE, DELETE ON vendasdb.{table} TO role_gerente;")
        time.sleep(0.5)
        
        # 3. Criar role_atendente - Apenas leitura em clientes e pedidos
        print("   Criando role_atendente...")
        db.execute_query("CREATE ROLE role_atendente;")
        
        # Conceder uso do schema
        db.execute_query("GRANT USAGE ON SCHEMA vendasdb TO role_atendente;")
        
        # Privilégios de leitura em customer, orders, orderitem
        atendente_tables = ['customer', 'orders', 'orderitem']
        for table in atendente_tables:
            db.execute_query(f"GRANT SELECT ON vendasdb.{table} TO role_atendente;")
        time.sleep(0.5)
        
        print("Roles criadas com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao criar roles: {e}")
        return False
    finally:
        db.disconnect()

def create_users():
    """Cria usuários e atribui roles"""
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    try:
        print("Criando usuários e atribuindo roles...")
        
        # Usar os mesmos usuários da tarefa01
        users_roles = [
            ('usr_a', 'usr_a123', 'role_adm'),      # 1 admin
            ('usr_b', 'usr_b123', 'role_gerente'),  # 1 gerente
            ('usr_c', 'usr_c123', 'role_atendente'), # 3 atendentes
            ('usr_d', 'usr_d123', 'role_atendente'),
            ('usr_e', 'usr_e123', 'role_atendente')
        ]
        
        for user, password, role in users_roles:
            print(f"   Atribuindo role {role} ao usuário {user}...")
            db.execute_query(f"GRANT {role} TO {user};")
            time.sleep(0.3)
        
        print("Usuários configurados com roles!")
        return True
        
    except Exception as e:
        print(f"Erro ao configurar usuários: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    if create_roles() and create_users():
        print("\nRoles e usuários configurados com sucesso!")