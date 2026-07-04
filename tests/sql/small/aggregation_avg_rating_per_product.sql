SELECT
    product_id,
    COUNT(*)     AS review_count,
    AVG(rating)  AS avg_rating,
    MAX(rating)  AS max_rating,
    MIN(rating)  AS min_rating
FROM small_reviews
GROUP BY product_id
ORDER BY avg_rating DESC;
