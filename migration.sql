CREATE TABLE `photo_database_folders` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`title` VARCHAR(255) NOT NULL,
	`description` VARCHAR(255) NOT NULL,
	`create_datatime` DATETIME NOT NULL,
	`last_edit_datatime` DATETIME,
	PRIMARY KEY (`id`)
);

CREATE TABLE `photo_database_images` (
	`id` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`title` VARCHAR(255) NOT NULL,
	`description` VARCHAR(255) NOT NULL,
	`path` VARCHAR(255) NOT NULL UNIQUE,
	`load_datatime` DATETIME NOT NULL,
	`last_edit_datatime` DATETIME,
	PRIMARY KEY (`id`)
);

CREATE TABLE `photo_database_links` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`folder_id` INT NOT NULL,
	`image_id` INT NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `photo_database_links` ADD CONSTRAINT `photo_database_links_fk0` FOREIGN KEY (`folder_id`) REFERENCES `photo_database_folders`(`id`);

ALTER TABLE `photo_database_links` ADD CONSTRAINT `photo_database_links_fk1` FOREIGN KEY (`image_id`) REFERENCES `photo_database_images`(`id`);



CREATE VIEW vs10 AS 
SELECT 
photo_database_images.id as "id", 
photo_database_images.title as "title",
photo_database_images.description as "description", 
photo_database_images.load_datatime as "load_datetime", 
photo_database_folders.title as "folder_title"
FROM photo_database_images
LEFT JOIN photo_database_links
ON photo_database_images.id = photo_database_links.image_id
LEFT JOIN photo_database_folders
ON photo_database_folders.id = photo_database_links.folder_id;