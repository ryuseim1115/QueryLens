SELECT
    u.id,
    u.name,
    (
        SELECT COUNT(*)
        FROM orders AS o
        WHERE o.user_id = u.id
    ) AS order_count,
    (
        SELECT COALESCE(SUM(o.amount), 0)
        FROM orders AS o
        WHERE o.user_id = u.id
    ) AS total_amount
FROM users AS u
ORDER BY total_amount DESC;
