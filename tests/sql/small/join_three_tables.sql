SELECT
    u.name         AS user_name,
    p.name         AS product_name,
    p.category,
    o.quantity,
    o.amount,
    o.status,
    o.order_date
FROM small_orders AS o
INNER JOIN small_users    AS u ON o.user_id    = u.id
INNER JOIN small_products AS p ON o.product_id = p.id
ORDER BY o.order_date;
