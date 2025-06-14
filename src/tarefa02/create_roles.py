from database_connection import DatabaseConnection

def create_roles():
    """Cria as roles para o sistema VENDASDB"""
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    try:
        print("Criando roles...")
        
        # 1. Criar role_adm - Acesso total
        print("   Criando role_adm...")
        db.execute_query("CREATE ROLE role_adm;")
        
        # Conceder uso do schema
        db.execute_query("GRANT USAGE ON SCHEMA vendasdb TO role_adm;")
        
        # Privilégios completos em todas as tabelas
        tables = ['customer', 'supplier', 'product', 'orders', 'orderitem']
        for table in tables:
            db.execute_query(f"GRANT ALL PRIVILEGES ON vendasdb.{table} TO role_adm;")
        
        # 2. Criar role_gerente - Acesso a fornecedores, produtos e pedidos
        print("   Criando role_gerente...")
        db.execute_query("CREATE ROLE role_gerente;")
        
        # Conceder uso do schema
        db.execute_query("GRANT USAGE ON SCHEMA vendasdb TO role_gerente;")
        
        # Privilégios de leitura e escrita em supplier, product, orders, orderitem
        gerente_tables = ['supplier', 'product', 'orders', 'orderitem']
        for table in gerente_tables:
            db.execute_query(f"GRANT SELECT, INSERT, UPDATE, DELETE ON vendasdb.{table} TO role_gerente;")
        
        # 3. Criar role_atendente - Apenas leitura em clientes e pedidos
        print("   Criando role_atendente...")
        db.execute_query("CREATE ROLE role_atendente;")
        
        # Conceder uso do schema
        db.execute_query("GRANT USAGE ON SCHEMA vendasdb TO role_atendente;")
        
        # Privilégios de leitura em customer, orders, orderitem
        atendente_tables = ['customer', 'orders', 'orderitem']
        for table in atendente_tables:
            db.execute_query(f"GRANT SELECT ON vendasdb.{table} TO role_atendente;")
        
        print("Roles criadas com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao criar roles: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    create_roles()