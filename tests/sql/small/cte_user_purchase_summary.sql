WITH user_orders AS (
    SELECT
        user_id,
        COUNT(*)    AS order_count,
        SUM(amount) AS total_amount
    FROM small_orders
    GROUP BY user_id
),
user_reviews AS (
    SELECT
        user_id,
        COUNT(*)    AS review_count,
        AVG(rating) AS avg_rating
    FROM small_reviews
    GROUP BY user_id
)
SELECT
    u.id,
    u.name,
    u.country,
    COALESCE(uo.order_count,  0) AS order_count,
    COALESCE(uo.total_amount, 0) AS total_amount,
    COALESCE(ur.review_count, 0) AS review_count,
    COALESCE(ur.avg_rating,   0) AS avg_rating
FROM small_users AS u
LEFT JOIN user_orders  AS uo ON u.id = uo.user_id
LEFT JOIN user_reviews AS ur ON u.id = ur.user_id
ORDER BY total_amount DESC;
