

-- ###
DROP KEYSPACE IF EXISTS shop;



-- keyspace з найпростішої стратегією реплікації 
-- ###
CREATE KEYSPACE shop
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};



-- ###
USE shop;



-- ###
DESCRIBE KEYSPACE shop;



-- Створення таблиці items
-- ###
DROP TABLE IF EXISTS items;
CREATE TABLE items(
    id UUID,
    name TEXT,
    category TEXT,
    price DECIMAL,
    producer TEXT,
    attributes MAP<TEXT, TEXT>,
    PRIMARY KEY (category, price, id)
) WITH CLUSTERING ORDER BY (price ASC);



-- Перевірка структури таблиці
-- ###
DESCRIBE TABLE items;



-- Заповнення таблиці items
-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('electronics', uuid(), 'Smartphone X', 999.99, 'Samsung', {'color': 'black', 'storage': '128GB', 'screen_size': '6.1 inch'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('electronics', uuid(), 'Smartphone Y', 799.99, 'Samsung', {'color': 'blue', 'storage': '256GB', 'screen_size': '6.5 inch'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('electronics', uuid(), 'Laptop Pro', 1299.99, 'Dell', {'cpu': 'Intel i7', 'ram': '16GB', 'storage': '512GB SSD'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('electronics', uuid(), 'Smart TV 55"', 699.99, 'Sony', {'resolution': '4K', 'screen_size': '55 inch', 'smart': 'Yes'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('electronics', uuid(), 'Wireless Headphones', 199.99, 'Bose', {'color': 'white', 'battery_life': '20h', 'noise_cancellation': 'Yes'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('electronics', uuid(), 'Gaming Console', 499.99, 'Microsoft', {'color': 'black', 'storage': '1TB', 'controller': 'Wireless'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('home_appliances', uuid(), 'Refrigerator XL', 1499.99, 'LG', {'capacity': '500L', 'energy_class': 'A++', 'color': 'silver'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('home_appliances', uuid(), 'Washing Machine 8kg', 799.99, 'Bosch', {'capacity': '8kg', 'spin_speed': '1400 rpm', 'color': 'white'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('home_appliances', uuid(), 'Microwave Oven', 299.99, 'Samsung', {'power': '900W', 'capacity': '25L', 'color': 'black'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('home_appliances', uuid(), 'Air Conditioner', 999.99, 'Daikin', {'cooling_power': '2.5kW', 'energy_class': 'A+', 'smart_control': 'Yes'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('home_appliances', uuid(), 'Vacuum Cleaner', 249.99, 'Dyson', {'power': '750W', 'cordless': 'Yes', 'filter': 'HEPA'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('furniture', uuid(), 'Sofa 3-seater', 1199.99, 'IKEA', {'material': 'leather', 'color': 'brown', 'dimensions': '220x90x80cm'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('furniture', uuid(), 'Dining Table', 899.99, 'WoodArt', {'material': 'oak wood', 'seats': '6', 'dimensions': '180x90x75cm'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('furniture', uuid(), 'Office Chair', 399.99, 'ErgoSeat', {'material': 'mesh', 'adjustable_height': 'Yes', 'color': 'black'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('furniture', uuid(), 'Wardrobe 4-door', 1299.99, 'HomeStyle', {'material': 'MDF', 'color': 'white', 'dimensions': '240x60x210cm'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('furniture', uuid(), 'Bed King Size', 1599.99, 'SleepWell', {'material': 'solid wood', 'mattress_size': '180x200cm', 'storage': 'Yes'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('sports', uuid(), 'Treadmill', 899.99, 'ProForm', {'motor_power': '3HP', 'max_speed': '20km/h', 'foldable': 'Yes'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('sports', uuid(), 'Exercise Bike', 499.99, 'NordicTrack', {'resistance_levels': '20', 'display': 'LCD', 'heart_rate_monitor': 'Yes'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('sports', uuid(), 'Dumbbell Set', 199.99, 'GymPro', {'weight_range': '5-30kg', 'adjustable': 'Yes', 'material': 'steel'});

-- ###
INSERT INTO items (category, id, name, price, producer, attributes) 
VALUES ('sports', uuid(), 'Yoga Mat', 49.99, 'Liforme', {'material': 'eco-friendly', 'thickness': '5mm', 'color': 'purple'});



-- ###
SELECT * FROM items;



-- Q1. Запит на отримання всіх товарів у певній категорії, відсортованих за ціною
-- ###
SELECT category, name, price, producer, attributes FROM items WHERE category = 'electronics';


-- Пошук товару за назвою в межах категорії
-- ###
CREATE MATERIALIZED VIEW items_by_name AS
SELECT category, name, price, producer, id, attributes
FROM items
WHERE category IS NOT NULL AND name IS NOT NULL AND price IS NOT NULL AND id IS NOT NULL
PRIMARY KEY (category, name, price, id);


-- Q2. Запит для отримання товару за назвою:
-- ###
SELECT category, name, price, producer, attributes FROM items_by_name WHERE category = 'electronics' AND name = 'Smartphone X';


-- Пошук товарів за ціною в межах діапазону*
-- ###
CREATE MATERIALIZED VIEW items_by_price_range AS
SELECT category, price, name, producer, id, attributes
FROM items
WHERE category IS NOT NULL AND price IS NOT NULL AND id IS NOT NULL
PRIMARY KEY (category, price, id);


-- Q3. Запит для отримання товарів у певному ціновому діапазоні:
-- ###
SELECT category, name, price, producer, attributes FROM items_by_price_range WHERE category = 'electronics' AND price >= 500 AND price <= 1000;



-- Пошук товарів за ціною та виробником у межах категорії**
-- ###
CREATE MATERIALIZED VIEW items_by_price_and_producer AS
SELECT category, price, producer, name, id, attributes
FROM items
WHERE category IS NOT NULL AND producer IS NOT NULL AND price IS NOT NULL AND id IS NOT NULL
PRIMARY KEY (category, producer, price, id);


-- Q4. Запит для отримання товарів за ціною та виробником:
-- ###
SELECT category, name, price, producer, attributes FROM items_by_price_and_producer WHERE category = 'electronics' AND producer = 'Samsung' AND price <= 1500;


-- ======================================================================


-- Створення таблиці orders
-- ###
CREATE TABLE orders (
    customer_name TEXT,
    order_date TIMESTAMP,
    order_id UUID,
    item_ids LIST<UUID>,
    cost DECIMAL,
    PRIMARY KEY (customer_name, order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date ASC);



-- Перевірка структури таблиці
-- ###
DESCRIBE TABLE orders;


-- ###
INSERT INTO orders (customer_name, order_id, item_ids, cost, order_date) VALUES ('John Doe', uuid(), [uuid(), uuid()], 1599.99, '2024-03-01 10:30:00');
INSERT INTO orders (customer_name, order_id, item_ids, cost, order_date) VALUES ('John Doe', uuid(), [uuid()], 499.99, '2024-03-05 14:15:00');
INSERT INTO orders (customer_name, order_id, item_ids, cost, order_date) VALUES ('Alice Smith', uuid(), [uuid()], 199.99, '2024-03-06 12:00:00');
INSERT INTO orders (customer_name, order_id, item_ids, cost, order_date) VALUES ('Bob Johnson', uuid(), [uuid(), uuid()], 1099.50, '2024-03-04 16:20:00');
INSERT INTO orders (customer_name, order_id, item_ids, cost, order_date) VALUES ('Bob Johnson', uuid(), [uuid()], 249.99, '2024-03-07 09:40:00');
INSERT INTO orders (customer_name, order_id, item_ids, cost, order_date) VALUES ('John Doe', uuid(), [uuid()], 149.99, '2024-03-08 07:30:00');


-- ###
SELECT * FROM orders;


-- Виведення всіх замовлень певного замовника, відсортованих за датою
-- ###
SELECT * FROM orders WHERE customer_name = 'John Doe';


-- Визначення суми усіх замовлень кожного клієнта
-- ###
SELECT customer_name, SUM(cost) AS total_spent FROM orders GROUP BY customer_name;


-- Виведення часу, коли була записана ціна замовлення
-- ###
SELECT order_id, cast(WRITETIME(cost) as date) AS write_time FROM orders;
