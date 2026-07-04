SELECT
    u.id,
    u.name,
    o.id     AS order_id,
    o.amount
FROM users AS u
LEFT JOIN orders AS o ON u.id = o.user_id
ORDER BY u.id, o.id;
