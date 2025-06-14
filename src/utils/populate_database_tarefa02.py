from database_connection import DatabaseConnection

def populate_vendasdb():
    """Popula o banco VENDASDB com dados baseados no popular_vendasbd.sql"""
    db = DatabaseConnection()
    conn = db.connect()
    
    if not conn:
        return False
    
    try:
        print("Populando banco VENDASDB...")
        
        # 1. Inserir CUSTOMERS
        print("   Inserindo customers...")
        customers_data = [
            (1,'Maria','Anfefeefeders','Berlin','Germany','030-0074321'),
            (2,'Ana','Truefeejillo','México D.F.','Mexico','(56) 555-4729'),
            (3,'Antonio','Moreddno','México D.F.','Mexico','(56) 555-3932'),
            (4,'Thomas','Hadddrdy','London','UK','(256) 555-7788'),
            (5,'Christina','Beddfrglund','Luleå','Sweden','0921-12 34 65'),
            (6,'Hanna','Moos','Mannhddddseim','Germany','0621-08460'),
            (7,'Frédérique','Citgggdeseaux','Strasbourg','France','88.60.15.31'),
            (8,'Martín','Sommfefer','Madrid','Spain','(91) 555 22 82'),
            (9,'Laurence','Lefefebihan','Marseille','France','91.24.45.40'),
            (10,'Elizabeth','Lifefessncoln','Tsawassen','Canada','(604) 555-4729'),
            (11,'Victoria','Ashscceworth','London','UK','(256) 555-1212'),
            (12,'Patricio','Siggrmpson','Buenos Aires','Argentina','(1) 135-5555'),
            (13,'Francisco','Chggrggrang','México D.F.','Mexico','(5) 555-3392'),
            (14,'Yang','Waggrng','Bern','Switzerland','0452-076545'),
            (15,'Pedro','Afddronso','Sao Paulo','Brazil','(11) 555-7647'),
            (16,'Elizabeth','Brvvdown','London','UK','(256) 555-2282'),
            (17,'Sven','Ottffvflieb','Aachen','Germany','0241-039123'),
            (18,'Janine','Labvvfrune','Nantes','France','40.67.88.88'),
            (19,'Ann','Devfvfon','London','UK','(256) 555-0297'),
            (20,'Roland','Menffvdel','Graz','Austria','7675-3425')
        ]
        
        for customer in customers_data:
            db.execute_query(
                "INSERT INTO vendasdb.customer (id, firstname, lastname, city, country, phone) VALUES (%s, %s, %s, %s, %s, %s)",
                customer
            )
        
        # 2. Inserir SUPPLIERS
        print("   Inserindo suppliers...")
        suppliers_data = [
            (1,'Exotic Liquids','CharlDDDDSotte Cooper','London','UK','(56) 555-2222',None),
            (2,'New Orleans Cajun Delights','ShelDDDSSley Burke','New Orleans','USA','(100) 555-4822',None),
            (3,'Grandma Kelly\'s Homestead','RegEEWina Murphy','Ann Arbor','USA','(313) 555-5735','(313) 555-3349'),
            (4,'Tokyo Traders','YosEEEhi Nagase','Tokyo','Japan','(03) 3555-5011',None),
            (5,'Cooperativa de Quesos \'Las Cabras\'','AntoEEenio del Valle Saavedra','Oviedo','Spain','(98) 598 76 54',None),
            (6,'Mayumi\'s','Mayueedfemi Ohno','Osaka','Japan','(06) 431-7877',None),
            (7,'Pavlova, Ltd.','Ian Devefeling','Melbourne','Australia','(03) 444-2343','(03) 444-6588'),
            (8,'Specialty Biscuits, Ltd.','Peter Wilsefeon','Manchester','UK','(161) 555-4448',None),
            (9,'PB Knäckebröd AB','Lars Peterefeson','Göteborg','Sweden','031-987 65 43','031-987 65 91'),
            (10,'Refrescos Americanas LTDA','Carlos Diafefez','Sao Paulo','Brazil','(56) 555 4640',None)
        ]
        
        for supplier in suppliers_data:
            db.execute_query(
                "INSERT INTO vendasdb.supplier (id, companyname, contactname, city, country, phone, fax) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                supplier
            )
        
        # 3. Inserir PRODUCTS
        print("   Inserindo products...")
        products_data = [
            (1,'Chai',1,18.00,'10 boxes x 20 bags',False),
            (2,'Chang',1,19.00,'24 - 12 oz bottles',False),
            (3,'Aniseed Syrup',1,10.00,'12 - 550 ml bottles',False),
            (4,'Chef Anton\'s Cajun Seasoning',2,22.00,'48 - 6 oz jars',False),
            (5,'Chef Anton\'s Gumbo Mix',2,21.35,'36 boxes',True),
            (6,'Grandma\'s Boysenberry Spread',3,25.00,'12 - 8 oz jars',False),
            (7,'Uncle Bob\'s Organic Dried Pears',3,30.00,'12 - 1 lb pkgs.',False),
            (8,'Northwoods Cranberry Sauce',3,40.00,'12 - 12 oz jars',False),
            (9,'Mishi Kobe Niku',4,97.00,'18 - 500 g pkgs.',True),
            (10,'Ikura',4,31.00,'12 - 200 ml jars',False),
            (11,'Queso Cabrales',5,21.00,'1 kg pkg.',False),
            (12,'Queso Manchego La Pastora',5,38.00,'10 - 500 g pkgs.',False),
            (13,'Konbu',6,6.00,'2 kg box',False),
            (14,'Tofu',6,23.25,'40 - 100 g pkgs.',False),
            (15,'Genen Shouyu',6,15.50,'24 - 250 ml bottles',False),
            (16,'Pavlova',7,17.45,'32 - 500 g boxes',False),
            (17,'Alice Mutton',7,39.00,'20 - 1 kg tins',True),
            (18,'Carnarvon Tigers',7,62.50,'16 kg pkg.',False),
            (19,'Teatime Chocolate Biscuits',8,9.20,'10 boxes x 12 pieces',False),
            (20,'Sir Rodney\'s Marmalade',8,81.00,'30 gift boxes',False)
        ]
        
        for product in products_data:
            db.execute_query(
                "INSERT INTO vendasdb.product (id, productname, supplierid, unitprice, package, isdiscontinued) VALUES (%s, %s, %s, %s, %s, %s)",
                product
            )
        
        # 4. Inserir ORDERS
        print("   Inserindo orders...")
        orders_data = [
            (1,'2012-01-01',78,1863.40,'542379'),
            (2,'2012-01-01',1,1813.00,'542380'),
            (3,'2012-01-01',4,670.80,'542381'),
            (4,'2012-01-02',6,3730.00,'542382'),
            (5,'2012-01-03',1,1444.80,'542383'),
            (6,'2012-01-04',14,625.20,'542384'),
            (7,'2012-01-01',8,2490.50,'542385'),
            (8,'2012-01-01',8,517.80,'542386'),
            (9,'2012-01-03',5,1119.90,'542387'),
            (10,'2012-01-04',20,2018.60,'542388')
        ]
        
        for order in orders_data:
            db.execute_query(
                "INSERT INTO vendasdb.orders (id, orderdate, customerid, totalamount, ordernumber) VALUES (%s, %s, %s, %s, %s)",
                order
            )
        
        # 5. Inserir ORDER ITEMS
        print("   Inserindo order items...")
        orderitems_data = [
            (1,1,11,14.00,12),
            (2,1,2,9.80,10),
            (3,1,18,34.80,5),
            (4,2,14,18.60,9),
            (5,2,11,42.40,40),
            (6,3,1,7.70,10),
            (7,3,11,42.40,35),
            (8,3,15,16.80,15),
            (9,4,2,16.80,6),
            (10,4,7,15.60,15),
            (11,4,15,16.80,20),
            (12,5,20,64.80,40),
            (13,5,3,2.00,25),
            (14,5,10,27.20,40),
            (15,6,1,10.00,20),
            (16,6,9,14.40,42),
            (17,6,19,16.00,40),
            (18,7,4,3.60,15),
            (19,7,15,19.20,21),
            (20,7,14,8.00,21)
        ]
        
        for item in orderitems_data:
            db.execute_query(
                "INSERT INTO vendasdb.orderitem (id, orderid, productid, unitprice, quantity) VALUES (%s, %s, %s, %s, %s)",
                item
            )
        
        print("VENDASDB populado com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao popular VENDASDB: {e}")
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    populate_vendasdb()
