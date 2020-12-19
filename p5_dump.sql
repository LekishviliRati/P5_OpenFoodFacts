-- MySQL Script generated by MySQL Workbench
-- Sun Dec  6 18:45:17 2020
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema p5_off
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema p5_off
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `p5_off` DEFAULT CHARACTER SET utf8 ;
USE `p5_off` ;

-- -----------------------------------------------------
-- Table `p5_off`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `p5_off`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p5_off`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `p5_off`.`product` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `description` TEXT(1000) NULL,
  `grade` TINYTEXT NOT NULL,
  `brand` VARCHAR(45) NOT NULL,
  `store` VARCHAR(45) NOT NULL,
  `url` VARCHAR(300) NOT NULL,
  `is_favorite` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p5_off`.`category_has_product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `p5_off`.`category_has_product` (
  `category_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  PRIMARY KEY (`category_id`, `product_id`),
  INDEX `fk_category_has_product_product1_idx` (`product_id` ASC) VISIBLE,
  INDEX `fk_category_has_product_category_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_category_has_product_category`
    FOREIGN KEY (`category_id`)
    REFERENCES `p5_off`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_category_has_product_product1`
    FOREIGN KEY (`product_id`)
    REFERENCES `p5_off`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
