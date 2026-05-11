CREATE DATABASE IF NOT EXISTS myapp;
USE myapp;

CREATE TABLE users(
id INT AUTO_INCREMENT PRIMARY KEY,
display_name VARCHAR(80) NOT NULL,
username VARCHAR(80) NOT NULL,
email VARCHAR(80) NOT NULL,
password_hash VARCHAR(100) NOT NULL,
bio VARCHAR(128) DEFAULT 'No bio yet',
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

INDEX idx_display_name (display_name),
INDEX idx_username (username),
INDEX idx_email (email),
INDEX idx_created_at (created_at)
);

CREATE TABLE posts(
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT NOT NULL,
image_filename VARCHAR(200) NOT NULL,
caption VARCHAR(100),
category VARCHAR(50),
tags VARCHAR(200),
visibility VARCHAR(20) DEFAULT 'public',
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,

INDEX idx_category (category),
INDEX idx_tags (tags),
INDEX idx_visibility (visibility),
INDEX idx_created_at (created_at)
);