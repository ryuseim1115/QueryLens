SELECT
    p.category,
    COUNT(o.id)  AS order_count,
    SUM(o.amount) AS total_sales
FROM products AS p
INNER JOIN orders AS o ON p.id = o.product_id
GROUP BY p.category
ORDER BY total_sales DESC;
