WITH user_orders AS (
    SELECT
        user_id,
        COUNT(*)    AS order_count,
        SUM(amount) AS total_amount
    FROM orders
    GROUP BY user_id
),
user_points AS (
    SELECT
        user_id,
        SUM(point_change) AS total_points
    FROM point_history
    GROUP BY user_id
)
SELECT
    u.id,
    u.name,
    COALESCE(uo.order_count,  0) AS order_count,
    COALESCE(uo.total_amount, 0) AS total_amount,
    COALESCE(up.total_points, 0) AS total_points
FROM users AS u
LEFT JOIN user_orders AS uo ON u.id = uo.user_id
LEFT JOIN user_points AS up ON u.id = up.user_id
ORDER BY total_amount DESC;
