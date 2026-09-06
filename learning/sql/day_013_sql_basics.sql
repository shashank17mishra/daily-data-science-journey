-- Day 013: SQL Basics, Filtering, and Aggregations
-- Schema Definition and Query Exercise for Customer Orders Analysis

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    country TEXT NOT NULL,
    created_at DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    status TEXT NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Analytical Query: High-value completed orders by European customers
SELECT 
    c.customer_name,
    c.country,
    COUNT(o.order_id) AS total_orders,
    SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'COMPLETED'
  AND c.country IN ('Germany', 'France', 'UK')
GROUP BY c.customer_id, c.customer_name, c.country
HAVING SUM(o.amount) >= 500.0
ORDER BY total_spent DESC;
