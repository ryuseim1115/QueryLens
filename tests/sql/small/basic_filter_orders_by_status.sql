SELECT id, user_id, product_id, amount, status, order_date
FROM small_orders
WHERE status IN ('delivered', 'shipped')
ORDER BY order_date;
