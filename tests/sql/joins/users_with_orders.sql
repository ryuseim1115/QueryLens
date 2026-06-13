SELECT
    u.id    AS user_id,
    u.name  AS user_name,
    o.id    AS order_id,
    o.amount,
    o.order_date
FROM users AS u
INNER JOIN orders AS o ON u.id = o.user_id
ORDER BY o.order_date;
