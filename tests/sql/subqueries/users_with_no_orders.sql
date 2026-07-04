SELECT id, name, email
FROM users
WHERE id NOT IN (
    SELECT DISTINCT user_id
    FROM orders
)
ORDER BY id;
