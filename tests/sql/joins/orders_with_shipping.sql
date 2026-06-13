SELECT
    o.id    AS order_id,
    o.user_id,
    o.amount,
    s.status,
    s.shipped_date,
    s.delivered_date
FROM orders AS o
LEFT JOIN shipping AS s ON o.id = s.order_id
ORDER BY o.id;
