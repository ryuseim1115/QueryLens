WITH product_orders AS (
    SELECT
        p.category,
        o.amount
    FROM small_products AS p
    INNER JOIN small_orders AS o ON p.id = o.product_id
),
category_summary AS (
    SELECT
        category,
        COUNT(*)    AS order_count,
        SUM(amount) AS total_sales
    FROM product_orders
    GROUP BY category
)
SELECT
    category,
    order_count,
    total_sales,
    ROUND(total_sales * 100.0 / SUM(total_sales) OVER (), 1) AS sales_ratio_pct
FROM category_summary
ORDER BY total_sales DESC;
