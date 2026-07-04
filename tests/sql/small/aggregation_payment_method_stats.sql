SELECT
    payment_method,
    COUNT(*)    AS tx_count,
    SUM(amount) AS total_amount
FROM small_transactions
GROUP BY payment_method
ORDER BY total_amount DESC;
