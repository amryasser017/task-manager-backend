CREATE DATABASE taskmanager;
USE taskmanager;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT NOW()
);

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status ENUM('pending', 'completed') DEFAULT 'pending',
    created_at DATETIME DEFAULT NOW(),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

USE taskmanager;

INSERT INTO users (username, email, password) 
VALUES ('amr', 'amr@test.com', 'test123');

ALTER TABLE tasks DROP FOREIGN KEY tasks_ibfk_1;

ALTER TABLE tasks MODIFY user_id INT NULL DEFAULT NULL;

USE taskmanager;
ALTER TABLE tasks ADD CONSTRAINT tasks_ibfk_1 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

USE taskmanager;
DELETE FROM users WHERE id > 0;


USE taskmanager;
SELECT * FROM users;