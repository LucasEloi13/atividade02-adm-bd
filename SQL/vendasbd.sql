-- -----------------------------------------------------
-- Schema VENDASDB
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `VENDASDB` ;
CREATE SCHEMA `VENDASDB` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `VENDASDB`;

SET NAMES 'utf8mb4';
SET CHARACTER SET utf8mb4;

-- -----------------------------------------------------
-- Table `CLIENTE`.`Supplier`
-- -----------------------------------------------------
CREATE TABLE  IF NOT EXISTS `VENDASDB`.`Supplier` (
  `id` int NOT NULL ,
  `companyname` varchar(40)  NULL,
  `contactname` varchar(50)  NULL,
  `contacttitle` varchar(40) NULL,
  `city` varchar(40)  NULL,
  `country` varchar(40) NULL,
  `phone` varchar(30)  NULL,
  `fax` varchar(30) NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- -----------------------------------------------------
-- Table `CLIENTE`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `VENDASDB`.`Product` (
  `id` INT NOT NULL ,
  `productname` VARCHAR(50) NULL,
  `supplierid` INT NOT NULL,
  `unitprice` DECIMAL(12,2) NULL,
  `package` VARCHAR(30) NULL,
  `isdiscontinued` BIT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_product_Supplier1_idx` (`supplierid` ASC) VISIBLE,
  CONSTRAINT `fk_product_Supplier1`
    FOREIGN KEY (`supplierid`)
    REFERENCES `VENDASDB`.`Supplier` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- -----------------------------------------------------
-- Table `CLIENTE`.`customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `VENDASDB`.`Customer` (
  `id` INT NOT NULL ,
  `firstname` VARCHAR(40) NULL,
  `lastname` VARCHAR(40) NULL,
  `city` VARCHAR(40) NULL,
  `country` VARCHAR(40) NULL,
  `phone` VARCHAR(20) NULL,
  PRIMARY KEY (`id`)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- -----------------------------------------------------
-- Table `CLIENTE`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `VENDASDB`.`Orders` (
  `id` INT NOT NULL ,
  `orderdate` DATETIME NULL,
  `ordernumber` VARCHAR(10) NULL,
  `customerid` INT NOT NULL,
  `totalamount` DECIMAL(12,2) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_order_customer1_idx` (`customerid` ASC) VISIBLE,
  CONSTRAINT `fk_order_customer1`
    FOREIGN KEY (`customerid`)
    REFERENCES `VENDASDB`.`Customer` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- -----------------------------------------------------
-- Table `CLIENTE`.`OrderItem`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `VENDASDB`.`OrderItem` (
  `id` INT NOT NULL ,
  `orderid` INT NOT NULL,
  `productid` INT NOT NULL,
  `unitprice` DECIMAL(12,2) NULL,
  `quantity` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_orderitem_product1_idx` (`productid` ASC) VISIBLE,
  INDEX `fk_orderitem_order1_idx` (`orderid` ASC) VISIBLE,
  CONSTRAINT `fk_orderitem_product1`
    FOREIGN KEY (`productid`)
    REFERENCES `VENDASDB`.`Product` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_orderitem_order1`
    FOREIGN KEY (`orderid`)
    REFERENCES `VENDASDB`.`Orders` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



