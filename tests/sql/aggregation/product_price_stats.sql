SELECT
    category,
    COUNT(*)       AS product_count,
    MIN(price)     AS min_price,
    MAX(price)     AS max_price,
    AVG(price)     AS avg_price,
    SUM(price)     AS total_price
FROM products
GROUP BY category
ORDER BY avg_price DESC;
