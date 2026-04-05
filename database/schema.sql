-- ============================================
-- Inventory Management System - Database Schema
-- ============================================

CREATE DATABASE IF NOT EXISTS inventory_db;
USE inventory_db;

-- Users table (authentication)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    quantity INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions table (IN/OUT stock movements)
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    type ENUM('IN', 'OUT') NOT NULL,
    quantity INT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- ============================================
-- Seed data: default admin user
-- Password: admin123 (bcrypt hashed)
-- ============================================
INSERT IGNORE INTO users (username, password_hash) VALUES
('admin', '$2b$12$KIXqbf0i8K4hMYmR3DRZxOMvDjrGUViFU6hGmXWAbMlOixMhFBOEO');

-- Seed sample products
INSERT IGNORE INTO products (id, name, category, price, quantity) VALUES
(1, 'Laptop Pro X1', 'Electronics', 1299.99, 25),
(2, 'Wireless Mouse', 'Electronics', 29.99, 150),
(3, 'Office Chair', 'Furniture', 349.99, 8),
(4, 'Notebook A4', 'Stationery', 4.99, 500),
(5, 'USB Hub 7-Port', 'Electronics', 39.99, 60),
(6, 'Desk Lamp LED', 'Furniture', 49.99, 5),
(7, 'Pen Set Blue', 'Stationery', 9.99, 200),
(8, 'Monitor 27"', 'Electronics', 399.99, 12);

-- Seed sample transactions
INSERT IGNORE INTO transactions (product_id, type, quantity, date) VALUES
(1, 'IN', 30, '2024-01-10'),
(1, 'OUT', 5, '2024-01-15'),
(2, 'IN', 200, '2024-01-08'),
(2, 'OUT', 50, '2024-01-20'),
(3, 'IN', 10, '2024-01-05'),
(3, 'OUT', 2, '2024-01-25'),
(4, 'IN', 600, '2024-01-03'),
(4, 'OUT', 100, '2024-01-18'),
(5, 'IN', 80, '2024-01-12'),
(5, 'OUT', 20, '2024-01-22');
