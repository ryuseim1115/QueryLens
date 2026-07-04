SELECT id, user_id, product_id, amount, order_date
FROM orders
WHERE amount >= 1000
  AND amount <= 3000
  AND order_date >= '2024-01-12'
ORDER BY order_date;
