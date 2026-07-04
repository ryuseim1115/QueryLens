SELECT
    u.name       AS user_name,
    p.name       AS product_name,
    p.category,
    o.amount,
    o.order_date
FROM orders AS o
INNER JOIN users    AS u ON o.user_id    = u.id
INNER JOIN products AS p ON o.product_id = p.id
ORDER BY o.order_date;
