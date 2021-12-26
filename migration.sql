CREATE TABLE `photo_database_folders` (
	`id` INT PRIMARY KEY AUTO_INCREMENT,
	`title` VARCHAR(255) NOT NULL,
	`description` VARCHAR(255) NOT NULL
);

CREATE TABLE `photo_database_images` (
	`id` INT PRIMARY KEY AUTO_INCREMENT,
	`title` VARCHAR(255) NOT NULL,
	`path` VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE `photo_database_links` (
	`id` INT PRIMARY KEY AUTO_INCREMENT,
	`folder_id` INT NOT NULL,
	`image_id` INT NOT NULL
);

ALTER TABLE `photo_database_links` ADD CONSTRAINT `photo_database_links_fk0` FOREIGN KEY (`folder_id`) REFERENCES `photo_database_folders`(`id`);

ALTER TABLE `photo_database_links` ADD CONSTRAINT `photo_database_links_fk1` FOREIGN KEY (`image_id`) REFERENCES `photo_database_images`(`id`);



CREATE OR REPLACE VIEW vsa11 AS 
SELECT 
photo_database_images.id as "photo_id", 
photo_database_images.title as "photo_title",
photo_database_folders.title as "folder_title",
photo_database_folders.id as "folder_id"
FROM photo_database_images
LEFT JOIN photo_database_links
ON photo_database_images.id = photo_database_links.image_id
LEFT JOIN photo_database_folders
ON photo_database_folders.id = photo_database_links.folder_id;