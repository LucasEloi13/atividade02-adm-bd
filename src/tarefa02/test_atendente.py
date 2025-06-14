import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.database_connection import DatabaseConnection

def test_atendente_permissions():
    """Testa permissões do atendente (usr_c, usr_d, usr_e)"""
    print("=== TESTANDO PERMISSÕES DOS ATENDENTES ===")
    
    atendentes = ['usr_c', 'usr_d', 'usr_e']
    
    for usuario in atendentes:
        print(f"\n--- Testando {usuario} ---")
        
        db = DatabaseConnection()
        db.user = usuario
        db.password = f'{usuario}123'
        conn = db.connect()
        
        if not conn:
            print(f"Falha ao conectar como {usuario}")
            continue
        
        try:
            # Teste 1: Consultar clientes (deve funcionar)
            print(f"\nTeste 1: {usuario} - Consultar clientes")
            result = db.fetch_all("SELECT firstname, lastname FROM vendasdb.customer LIMIT 3;")
            if result:
                print(f"   SUCESSO: {usuario} conseguiu consultar clientes")
                for row in result:
                    print(f"     - {row['firstname']} {row['lastname']}")
            time.sleep(1)
            
            # Teste 2: Consultar pedidos (deve funcionar)
            print(f"\nTeste 2: {usuario} - Consultar pedidos")
            result = db.fetch_all("SELECT id, totalamount, ordernumber FROM vendasdb.orders LIMIT 3;")
            if result:
                print(f"   SUCESSO: {usuario} conseguiu consultar pedidos")
                for row in result:
                    print(f"     - Pedido #{row['id']}: R$ {row['totalamount']} ({row['ordernumber']})")
            time.sleep(1)
            
            # Teste 3: Tentar excluir fornecedor (deve falhar)
            print(f"\nTeste 3: {usuario} - Tentar excluir fornecedor")

            db.execute_query("DELETE FROM vendasdb.supplier WHERE id = 999;")
            print(f"   ERRO ESPERADO: {usuario} não deve conseguir excluir fornecedor")

            time.sleep(1)
            
            # Teste 4: Tentar acessar produtos (deve falhar)
            print(f"\nTeste 4: {usuario} - Tentar acessar produtos")
            
            result = db.fetch_all("SELECT productname FROM vendasdb.product LIMIT 1;")
            print(f"   ERRO ESPERADO: {usuario} não deve conseguir acessar produtos")

            time.sleep(1)
            
            # Teste 5: Tentar modificar cliente (deve falhar)
            print(f"\nTeste 5: {usuario} - Tentar modificar cliente")

            db.execute_query("UPDATE vendasdb.customer SET firstname = 'Teste' WHERE id = 1;")
            print(f"   ERRO ESPERADO: {usuario} não deve conseguir modificar cliente")

            time.sleep(1)
            
        except Exception as e:
            print(f"Erro durante teste do {usuario}: {e}")
        finally:
            db.disconnect()

if __name__ == "__main__":
    test_atendente_permissions()
