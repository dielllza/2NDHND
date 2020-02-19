-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema 2ndhnd_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `2ndhnd_db` ;

-- -----------------------------------------------------
-- Schema 2ndhnd_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `2ndhnd_db` DEFAULT CHARACTER SET utf8 ;


USE `2ndhnd_db` ;

-- -----------------------------------------------------
-- Table `2ndhnd_db`.`categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `2ndhnd_db`.`categories` ;

CREATE TABLE IF NOT EXISTS `2ndhnd_db`.`categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8;
INSERT INTO categories(category_name)
VALUES ('fashion'),
		('house_and_appliances'),
		('technology'),
        ('cars'),
        ('sports'),
        ('books');

-- -----------------------------------------------------
-- Table `2ndhnd_db`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `2ndhnd_db`.`users` ;

CREATE TABLE IF NOT EXISTS `2ndhnd_db`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL DEFAULT NULL,
  `last_name` VARCHAR(255) NULL DEFAULT NULL,
  `email_address` VARCHAR(255) NULL DEFAULT NULL,
  `phone_number` VARCHAR(255) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `2ndhnd_db`.`products`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `2ndhnd_db`.`products` ;

CREATE TABLE IF NOT EXISTS `2ndhnd_db`.`products` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `users_id` INT(11) NOT NULL,
  `product_name` VARCHAR(255) NULL DEFAULT NULL,
  `categories_id` INT(11) NOT NULL,
  `price` DOUBLE NULL DEFAULT NULL,
  `product_description` TEXT NULL DEFAULT NULL,
  `image` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_products_users_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_products_categories1_idx` (`categories_id` ASC) VISIBLE,
  CONSTRAINT `fk_products_categories1`
    FOREIGN KEY (`categories_id`)
    REFERENCES `2ndhnd_db`.`categories` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_products_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `2ndhnd_db`.`users` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `2ndhnd_db`.`saves`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `2ndhnd_db`.`saves` ;

CREATE TABLE IF NOT EXISTS `2ndhnd_db`.`saves` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `product_id` INT(11) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_saves_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_saves_products1_idx` (`product_id` ASC) VISIBLE,
  CONSTRAINT `fk_saves_products1`
    FOREIGN KEY (`product_id`)
    REFERENCES `2ndhnd_db`.`products` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_saves_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `2ndhnd_db`.`users` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `2ndhnd_db`.`following_categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `2ndhnd_db`.`following_categories` ;

CREATE TABLE IF NOT EXISTS `2ndhnd_db`.`following_categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `category_id` INT(11) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_following_categories_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_following_categories_categories1_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_following_categories_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `2ndhnd_db`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_following_categories_categories1`
    FOREIGN KEY (`category_id`)
    REFERENCES `2ndhnd_db`.`categories` (`id`)
   ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
