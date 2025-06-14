import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection

def test_gerente_permissions():
    """Testa permissões do gerente (usr_b)"""
    print("=== TESTANDO PERMISSÕES DO GERENTE (usr_b) ===")
    
    db = DatabaseConnection()
    db.user = 'usr_b'
    db.password = 'usr_b123'
    conn = db.connect()
    
    if not conn:
        print("Falha ao conectar como usr_b")
        return
    
    try:
        # Teste 1: Inserir produto (deve funcionar)
        print("\nTeste 1: Inserir produto")
        db.execute_query(
            "INSERT INTO vendasdb.product (id, productname, supplierid, unitprice, package, isdiscontinued) VALUES (%s, %s, %s, %s, %s, %s);",
            (998, 'Produto Gerente', 1, 79.99, '1 unit', False)
        )
        print("   SUCESSO: Gerente conseguiu inserir produto")
        time.sleep(1)
        
        # Teste 2: Consultar fornecedores (deve funcionar)
        print("\nTeste 2: Consultar fornecedores")
        result = db.fetch_all("SELECT companyname FROM vendasdb.supplier LIMIT 3;")
        if result:
            print("   SUCESSO: Gerente conseguiu consultar fornecedores")
            for row in result:
                print(f"     - {row['companyname']}")
        time.sleep(1)
        
        # Teste 3: Consultar pedidos (deve funcionar)
        print("\nTeste 3: Consultar pedidos")
        result = db.fetch_all("SELECT id, totalamount FROM vendasdb.orders LIMIT 3;")
        if result:
            print("   SUCESSO: Gerente conseguiu consultar pedidos")
            for row in result:
                print(f"     - Pedido #{row['id']}: R$ {row['totalamount']}")
        time.sleep(1)
        
        # Teste 4: Tentar acessar clientes (deve falhar)
        print("\nTeste 4: Tentar acessar clientes")
        
        result = db.fetch_all("SELECT firstname FROM vendasdb.customer LIMIT 1;")
        print("   ERRO ESPERADO: Gerente não deve conseguir acessar clientes")

        time.sleep(1)
        
        # Limpar teste
        db.execute_query("DELETE FROM vendasdb.product WHERE id = 998;")
        
    except Exception as e:
        print(f"Erro durante teste: {e}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    test_gerente_permissions()
