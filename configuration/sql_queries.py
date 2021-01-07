# -*- coding: utf-8 -*-
"""SQL queries"""

########################################################################################################################
#                                   << DATABASE QUERIES
########################################################################################################################


TABLES = {}

TABLES['category'] = ("CREATE TABLE IF NOT EXISTS `p5_off`.`category` ("
                      "`id` INT NOT NULL AUTO_INCREMENT,"
                      "`name` VARCHAR(45) NOT NULL,"
                      "PRIMARY KEY (`id`))"
                      "ENGINE = InnoDB;")


TABLES['product'] = ("CREATE TABLE IF NOT EXISTS `p5_off`.`product` ("
                     "`id` INT NOT NULL AUTO_INCREMENT,"
                     "`name` VARCHAR(45) NOT NULL,"
                     "`description` TEXT(1000) NULL,"
                     "`grade` TINYTEXT NOT NULL,"
                     "`brand` VARCHAR(45) NOT NULL,"
                     "`store` VARCHAR(45) NOT NULL,"
                     "`url` VARCHAR(300) NOT NULL,"
                     "`category` VARCHAR(300) NOT NULL,"
                     "`is_favorite` TINYINT(1) NOT NULL DEFAULT 0,"
                     "PRIMARY KEY (`id`))"
                     "ENGINE = InnoDB;")


TABLES['category_has_product'] = ("CREATE TABLE IF NOT EXISTS `p5_off`.`category_has_product` ("
                                  "`category_id` INT NOT NULL,"
                                  "`product_id` INT NOT NULL,"
                                  "PRIMARY KEY (`category_id`, `product_id`),"
                                  "INDEX `fk_category_has_product_product1_idx` (`product_id` ASC) VISIBLE,"
                                  "INDEX `fk_category_has_product_category_idx` (`category_id` ASC) VISIBLE,"
                                  "CONSTRAINT `fk_category_has_product_category`"
                                  "FOREIGN KEY (`category_id`)"
                                  "REFERENCES `p5_off`.`category` (`id`),"
                                  "CONSTRAINT `fk_category_has_product_product1`"
                                  "FOREIGN KEY (`product_id`)"
                                  "REFERENCES `p5_off`.`product` (`id`))"
                                  "ENGINE = InnoDB;")


INSERT_PRODUCTS = ("INSERT IGNORE INTO product"
                   "(name, description, grade, brand, store, url, category) "
                   "VALUES (%(name)s, %(description)s, %(grade)s, %(brand)s, "
                   "%(store)s, %(url)s, %(category)s);")


INSERT_PRODUCT_CATEGORY = "INSERT INTO category_has_product " \
                          "(product_id, category_id) " \
                          "VALUES (" \
                          "%(product_id)s, %(category_id)s);"

SELECT_BEVERAGE_CATEGORY_ID = "SELECT id FROM category WHERE name = 'Boissons';"

SELECT_BEVERAGE_PRODUCT_ID = "SELECT id FROM product WHERE category = 'Boissons';"

SELECT_MEAL_CATEGORY_ID = "SELECT id FROM category WHERE name = 'Plats Préparés';"

SELECT_MEAL_PRODUCT_ID = "SELECT id FROM product WHERE category = 'Plats Préparés';"

SELECT_MEAT_CATEGORY_ID = "SELECT id FROM category WHERE name = 'Viandes';"

SELECT_MEAT_PRODUCT_ID = "SELECT id FROM product WHERE category = 'Viandes';"

SELECT_CHEESE_CATEGORY_ID = "SELECT id FROM category WHERE name = 'Fromages';"

SELECT_CHEESE_PRODUCT_ID = "SELECT id FROM product WHERE category = 'Fromages';"

SELECT_DESSERT_CATEGORY_ID = "SELECT id FROM category WHERE name = 'Desserts';"

SELECT_DESSERT_PRODUCT_ID = "SELECT id FROM product WHERE category = 'Desserts';"

########################################################################################################################
#                                   DATABASE QUERIES >>
########################################################################################################################


########################################################################################################################
#                                   << DISPLAY QUERIES
########################################################################################################################
SELECT_CATEGORIES = "SELECT "\
                    "category.id, category.name " \
                    "FROM category ;"\


SELECT_UNHEALTHY_PRODUCTS_FROM_CATEGORY = "SELECT product.id, product.name, product.description," \
                                "product.grade, product.brand, product.store, product.url " \
                                "FROM product "\
                                "LEFT JOIN category_has_product "\
                                "ON product.id=category_has_product.product_id "\
                                "RIGHT JOIN category "\
                                "ON category.id=category_has_product.category_id "\
                                "WHERE category.id = %s " \
                                "AND grade >= 'C';" \

PRODUCT_TO_SUBSTITUTE = "SELECT product.grade, product.category "\
                        "FROM product "\
                        "WHERE product.id = %s; "

SELECT_SUBSTITUTES = "SELECT product.id, product.name, product.description," \
                     "product.grade, product.brand, product.store, product.url, product.category " \
                     "FROM product "\
                     "WHERE product.category = %s "\
                     "AND product.grade < %s;"

SELECT_SUBSTITUTE = "SELECT * FROM product WHERE id = %s;"

UPDATE_TO_FAVORITE = "UPDATE product " \
                     "SET is_favorite=1 " \
                     "WHERE product.id = %s;"

UPDATE_TO_NON_FAVORITE = "UPDATE product " \
                     "SET is_favorite=0 " \
                     "WHERE product.id = %s;"

SELECT_FAVORITE = "SELECT product.id, product.name, product.description, " \
                  "product.grade, product.brand, product.store, product.url, product.category " \
                  "FROM product " \
                  "WHERE product.is_favorite = 1;"

CLEAN_FAVORITE_LIST = "UPDATE product " \
                     "SET is_favorite=0;"

########################################################################################################################
#                                    DISPLAY QUERIES  >>
########################################################################################################################