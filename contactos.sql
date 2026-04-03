CREATE DATABASE IF NOT EXISTS mini_contactos;
USE mini_contactos;

CREATE TABLE IF NOT EXISTS contacto (
id INT AUTO_INCREMENT PRIMARY KEY;    
numero INT UNIQUE NOT NULL;
nombre VARCHAR (50) UNIQUE NOT NULL;
email VARCHAR (70) UNIQUE NOT NULL;
CREATE_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
)

INSER INTO contacto (nombre,numero,email) VALUES 
('Ana García', '555-1234', 'ana@email.com'),
('Luis Pérez', '555-5678', 'luis@email.com'),
('María López', '555-9012', 'maria@email.com');


