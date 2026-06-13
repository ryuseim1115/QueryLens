SELECT id, user_id, product_id, amount, order_date
FROM orders
WHERE amount > 2000
ORDER BY amount DESC;
