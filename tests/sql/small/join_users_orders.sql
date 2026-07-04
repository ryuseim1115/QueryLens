SELECT
    u.id        AS user_id,
    u.name      AS user_name,
    u.country,
    o.id        AS order_id,
    o.amount,
    o.status,
    o.order_date
FROM small_users AS u
INNER JOIN small_orders AS o ON u.id = o.user_id
ORDER BY o.order_date;
