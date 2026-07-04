WITH user_spend AS (
    SELECT
        user_id,
        SUM(amount)  AS total_amount,
        COUNT(*)     AS order_count
    FROM orders
    GROUP BY user_id
),
top_spenders AS (
    SELECT user_id
    FROM user_spend
    WHERE total_amount >= (SELECT AVG(total_amount) FROM user_spend)
)
SELECT
    u.id,
    u.name,
    us.total_amount,
    us.order_count
FROM users AS u
INNER JOIN user_spend  AS us ON u.id = us.user_id
INNER JOIN top_spenders AS ts ON u.id = ts.user_id
ORDER BY us.total_amount DESC;
