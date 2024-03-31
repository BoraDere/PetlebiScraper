CREATE DATABASE IF NOT EXISTS petlebi;

USE petlebi;

CREATE TABLE IF NOT EXISTS petlebi (
    product_url VARCHAR(255),
    product_name VARCHAR(255),
    product_barcode VARCHAR(50),
    product_price VARCHAR(50),
    product_stock VARCHAR(50),
    product_images TEXT,
    description TEXT,
    sku VARCHAR(50),
    category TEXT,
    product_id INT PRIMARY KEY,
    brand VARCHAR(255)
);