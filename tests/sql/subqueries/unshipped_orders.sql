SELECT
    o.id    AS order_id,
    o.user_id,
    o.amount,
    o.order_date
FROM orders AS o
WHERE o.id NOT IN (
    SELECT order_id
    FROM shipping
    WHERE status = 'delivered'
)
ORDER BY o.order_date;
