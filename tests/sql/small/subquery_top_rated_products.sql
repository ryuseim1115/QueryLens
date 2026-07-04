SELECT
    p.id,
    p.name,
    p.category,
    r.avg_rating
FROM small_products AS p
INNER JOIN (
    SELECT product_id, AVG(rating) AS avg_rating
    FROM small_reviews
    GROUP BY product_id
) AS r ON p.id = r.product_id
WHERE r.avg_rating >= (SELECT AVG(rating) FROM small_reviews)
ORDER BY r.avg_rating DESC;
