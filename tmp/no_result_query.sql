SELECT u.id,
    u.name,
    u.email
FROM test1 u
    JOIN (
        SELECT id
        FROM test1
        WHERE age > 999
    ) sub ON u.id = sub.id