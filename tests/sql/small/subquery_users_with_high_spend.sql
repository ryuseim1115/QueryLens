SELECT
    u.id,
    u.name,
    u.country,
    spend.total_amount
FROM small_users AS u
INNER JOIN (
    SELECT user_id, SUM(amount) AS total_amount
    FROM small_orders
    GROUP BY user_id
) AS spend ON u.id = spend.user_id
WHERE spend.total_amount > (
    SELECT AVG(total_amount)
    FROM (
        SELECT SUM(amount) AS total_amount
        FROM small_orders
        GROUP BY user_id
    ) AS avg_sub
)
ORDER BY spend.total_amount DESC;
