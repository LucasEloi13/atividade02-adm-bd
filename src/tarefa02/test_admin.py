import sys
import os
import time
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection

def test_admin_permissions():
    """Testa permissões do administrador (usr_a)"""
    print("=== TESTANDO PERMISSÕES DO ADMINISTRADOR (usr_a) ===")
    
    db = DatabaseConnection()
    db.user = 'usr_a'
    db.password = 'usr_a123'
    conn = db.connect()
    
    if not conn:
        print("Falha ao conectar como usr_a")
        return
    
    try:

        random_id = random.randint(0, 9999)
        # Teste 1: Acessar todas as tabelas
        print("\nTeste 1: Acessar todas as tabelas")
        tables = ['customer', 'supplier', 'product', 'orders', 'orderitem']
        
        for table in tables:
            result = db.fetch_all(f"SELECT COUNT(*) as total FROM vendasdb.{table};")
            if result:
                print(f"   SUCESSO: Admin acessou {table} - {result[0]['total']} registros")
            time.sleep(0.3)
        
        # Teste 2: Inserir cliente (deve funcionar)
        print("\nTeste 2: Inserir cliente")
        db.execute_query(
            "INSERT INTO vendasdb.customer (id, firstname, lastname, city, country, phone) VALUES (%s, %s, %s, %s, %s, %s);",
            (random_id, 'Admin', 'Test', 'São Paulo', 'Brazil', '11999999999')
        )
        print("   SUCESSO: Admin conseguiu inserir cliente")
        
        # Teste 3: Inserir produto (deve funcionar)
        print("\nTeste 3: Inserir produto")
        db.execute_query(
            "INSERT INTO vendasdb.product (id, productname, supplierid, unitprice, package, isdiscontinued) VALUES (%s, %s, %s, %s, %s, %s);",
            (random_id, 'Produto Admin', 1, 99.99, '1 unit', False)
        )
        print("   SUCESSO: Admin conseguiu inserir produto")
        
        # Teste 4: Excluir registros de teste
        print("\nTeste 4: Excluir registros de teste")
        db.execute_query(f"DELETE FROM vendasdb.customer WHERE id = {random_id};")
        db.execute_query(f"DELETE FROM vendasdb.product WHERE id = {random_id};")
        print("   SUCESSO: Admin conseguiu excluir registros")
        
    except Exception as e:
        print(f"Erro durante teste: {e}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    test_admin_permissions()
