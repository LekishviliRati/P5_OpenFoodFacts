# -*- coding: utf-8 -*-
"""SQL queries"""


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
