-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS task_manager;
USE task_manager;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de tareas
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insertar algunos datos de ejemplo
INSERT INTO users (username, email, password) VALUES 
('john_doe', 'john@example.com', 'password123'),
('jane_smith', 'jane@example.com', 'password456');

INSERT INTO tasks (user_id, title, description, status, priority, due_date) VALUES 
(1, 'Aprender MySQL', 'Estudiar fundamentos de MySQL y consultas SQL', 'in_progress', 'high', '2024-12-15'),
(1, 'Crear proyecto Python', 'Desarrollar aplicación de gestión de tareas', 'pending', 'high', '2024-12-20'),
(2, 'Revisar código', 'Hacer code review del proyecto', 'pending', 'medium', '2024-12-10');