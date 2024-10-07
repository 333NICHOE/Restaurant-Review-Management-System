CREATE DATABASE IF NOT EXISTS FoodReviewDB;
USE FoodReviewDB;

-- Table for ADMIN
CREATE TABLE ADMIN (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL
);

-- Table for CUSTOMER
CREATE TABLE CUSTOMER (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birthday DATE NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Table for FOOD_ESTABLISHMENT
CREATE TABLE FOOD_ESTABLISHMENT (
    establishment_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    barangay VARCHAR(100) NOT NULL,
    postal_code VARCHAR(25) NOT NULL,
    street_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    average_rating DECIMAL(2,1) NOT NULL DEFAULT 0, -- Initial value set to 0
    average_price DECIMAL(6,2) NOT NULL DEFAULT 0 -- Initial value set to 0
);

-- Table for FOOD_ITEM
CREATE TABLE FOOD_ITEM (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    price DECIMAL(6,2) NOT NULL,
    rating DECIMAL(2,1) NOT NULL DEFAULT 0, -- Initial value set to 0
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    food_type VARCHAR(100) NOT NULL, 
    establishment_id INT,
    FOREIGN KEY (establishment_id) REFERENCES FOOD_ESTABLISHMENT(establishment_id)
);

-- Table for FOOD_REVIEW
CREATE TABLE FOOD_REVIEW (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    review_date DATE NOT NULL,
    review_time TIME NOT NULL,
    type_of_review VARCHAR(50) NOT NULL,
    rating DECIMAL(2,1) NOT NULL DEFAULT 0,
    title VARCHAR(255) NOT NULL,
    suggestion TEXT NOT NULL,
    customer_id INT,
    establishment_id INT,
    food_id INT,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id),
    FOREIGN KEY (establishment_id) REFERENCES FOOD_ESTABLISHMENT(establishment_id),
    FOREIGN KEY (food_id) REFERENCES FOOD_ITEM(food_id)
);

-- Table for MEAT
CREATE TABLE MEAT (
    food_id INT,
    meat_type VARCHAR(100),
    FOREIGN KEY (food_id) REFERENCES FOOD_ITEM(food_id),
    PRIMARY KEY (food_id, meat_type)
);

-- Table for VEGETABLE
CREATE TABLE VEGETABLE (
    food_id INT,
    vegetable_type VARCHAR(100),
    FOREIGN KEY (food_id) REFERENCES FOOD_ITEM(food_id),
    PRIMARY KEY (food_id, vegetable_type)
);

-- Table for DESSERT
CREATE TABLE DESSERT (
    food_id INT,
    dessert_type VARCHAR(100),
    FOREIGN KEY (food_id) REFERENCES FOOD_ITEM(food_id),
    PRIMARY KEY (food_id, dessert_type)
);

INSERT INTO ADMIN (email, password, first_name, last_name) VALUES
('admin@admin.com', 'adminadmin', 'Admin', 'One');
