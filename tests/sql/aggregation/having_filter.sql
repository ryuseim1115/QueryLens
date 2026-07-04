SELECT
    user_id,
    COUNT(*)    AS order_count,
    SUM(amount) AS total_amount
FROM orders
GROUP BY user_id
HAVING COUNT(*) >= 2
ORDER BY total_amount DESC;
