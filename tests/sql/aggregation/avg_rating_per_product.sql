SELECT
    product_id,
    COUNT(*)      AS review_count,
    AVG(rating)   AS avg_rating
FROM reviews
GROUP BY product_id
HAVING COUNT(*) >= 1
ORDER BY avg_rating DESC;
