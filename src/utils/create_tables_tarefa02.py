from database_connection import DatabaseConnection

def create_tables_tarefa02():
    """Cria todas as tabelas do esquema VENDASDB (Tarefa 02)"""
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    # SQL para criação do schema e tabelas baseado no vendasbd.sql
    tables_sql = [
        """
        DROP SCHEMA IF EXISTS vendasdb CASCADE;
        """,
        
        """
        CREATE SCHEMA vendasdb;
        """,
        
        """
        CREATE TABLE vendasdb.supplier (
            id INTEGER PRIMARY KEY,
            companyname VARCHAR(40),
            contactname VARCHAR(50),
            contacttitle VARCHAR(40),
            city VARCHAR(40),
            country VARCHAR(40),
            phone VARCHAR(30),
            fax VARCHAR(30)
        );
        """,
        
        """
        CREATE TABLE vendasdb.product (
            id INTEGER PRIMARY KEY,
            productname VARCHAR(50),
            supplierid INTEGER NOT NULL,
            unitprice DECIMAL(12,2),
            package VARCHAR(30),
            isdiscontinued BOOLEAN,
            CONSTRAINT fk_product_supplier
                FOREIGN KEY (supplierid) REFERENCES vendasdb.supplier(id)
        );
        """,
        
        """
        CREATE TABLE vendasdb.customer (
            id INTEGER PRIMARY KEY,
            firstname VARCHAR(40),
            lastname VARCHAR(40),
            city VARCHAR(40),
            country VARCHAR(40),
            phone VARCHAR(20)
        );
        """,
        
        """
        CREATE TABLE vendasdb.orders (
            id INTEGER PRIMARY KEY,
            orderdate TIMESTAMP,
            ordernumber VARCHAR(10),
            customerid INTEGER NOT NULL,
            totalamount DECIMAL(12,2),
            CONSTRAINT fk_order_customer
                FOREIGN KEY (customerid) REFERENCES vendasdb.customer(id)
        );
        """,
        
        """
        CREATE TABLE vendasdb.orderitem (
            id INTEGER PRIMARY KEY,
            orderid INTEGER NOT NULL,
            productid INTEGER NOT NULL,
            unitprice DECIMAL(12,2),
            quantity INTEGER,
            CONSTRAINT fk_orderitem_product
                FOREIGN KEY (productid) REFERENCES vendasdb.product(id),
            CONSTRAINT fk_orderitem_order
                FOREIGN KEY (orderid) REFERENCES vendasdb.orders(id)
        );
        """
    ]
    
    try:
        print("Criando schema e tabelas do VENDASDB...")
        for sql in tables_sql:
            db.execute_query(sql)
        print("Schema VENDASDB e tabelas criadas com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    create_tables_tarefa02()
