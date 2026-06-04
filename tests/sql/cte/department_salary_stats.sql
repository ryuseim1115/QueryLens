WITH dept_stats AS (
    SELECT
        department,
        COUNT(*)    AS headcount,
        AVG(salary) AS avg_salary,
        MAX(salary) AS max_salary,
        MIN(salary) AS min_salary
    FROM employees
    GROUP BY department
)
SELECT
    department,
    headcount,
    ROUND(avg_salary, 0) AS avg_salary,
    max_salary,
    min_salary
FROM dept_stats
ORDER BY avg_salary DESC;
