SELECT
    p.id       AS product_id,
    p.name     AS product_name,
    p.category,
    r.rating,
    r.comment
FROM products AS p
INNER JOIN reviews AS r ON p.id = r.product_id
ORDER BY r.rating DESC;
