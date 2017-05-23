CREATE TABLE IF NOT EXISTS `black_cat_db`.`event_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`create_time` INT UNSIGNED NOT NULL,
	`start_date` INT UNSIGNED NOT NULL,
	`end_date` INT UNSIGNED NOT NULL,
	`title` VARCHAR(64) NOT NULL,
	`latitude` FLOAT(10,6) NOT NULL,
	`longitude` FLOAT(10,6) NOT NULL,
	`description` TEXT NOT NULL,
	PRIMARY KEY (`id`),
	INDEX idx_title (`title`),
	INDEX idx_start_date (`start_date`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `black_cat_db`.`image_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`event_id` BIGINT UNSIGNED NOT NULL,
	`file` VARCHAR(256) NOT NULL,
	PRIMARY KEY (`id`, `event_id`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `black_cat_db`.`user_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`create_time` INT UNSIGNED NOT NULL,
	`access_token` VARCHAR(1024) NULL,
	`email` VARCHAR(256) NOT NULL,
	`name` VARCHAR(64) NOT NULL,
	`password` VARCHAR(256) NOT NULL,
	`is_admin` TINYINT NOT NULL,
	PRIMARY KEY (`id`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `black_cat_db`.`category_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(64) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE INDEX (`name`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `black_cat_db`.`registration_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`user_id` BIGINT UNSIGNED NOT NULL,
	`event_id` BIGINT UNSIGNED NOT NULL,
	PRIMARY KEY (`id`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `black_cat_db`.`comment_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`user_id` BIGINT UNSIGNED NOT NULL,
	`event_id` BIGINT UNSIGNED NOT NULL,
	`create_time` INT UNSIGNED NOT NULL,
	`description` TEXT NOT NULL,
	PRIMARY KEY (`id`, `event_id`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `black_cat_db`.`like_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`user_id` BIGINT UNSIGNED NOT NULL,
	`event_id` BIGINT UNSIGNED NOT NULL,
	PRIMARY KEY (`id`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `black_cat_db`.`event_category_tab` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`category_id` BIGINT UNSIGNED NOT NULL,
	`event_id` BIGINT UNSIGNED NOT NULL,
	PRIMARY KEY (`id`)
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;
