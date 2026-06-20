import api.db.connection
import duckdb

_shared_connection = duckdb.connect()
_shared_connection.sql("""
    CREATE TABLE users AS SELECT * FROM (VALUES
        (1, '山田太郎', 'yamada@example.com', 28),
        (2, '鈴木花子', 'suzuki@example.com', 34),
        (3, '佐藤次郎', 'sato@example.com', 22),
        (4, '田中美咲', 'tanaka@example.com', 41),
        (5, '伊藤健一', 'ito@example.com', 19)
    ) t(id, name, email, age)
""")
_shared_connection.sql("""
    CREATE TABLE orders AS SELECT * FROM (VALUES
        (1, 1, 3, 1500, '2024-01-10'),
        (2, 2, 1, 3200, '2024-01-11'),
        (3, 1, 2, 800,  '2024-01-12'),
        (4, 3, 3, 1500, '2024-01-13'),
        (5, 4, 1, 3200, '2024-01-14'),
        (6, 2, 2, 800,  '2024-01-15'),
        (7, 5, 3, 1500, '2024-01-16')
    ) t(id, user_id, product_id, amount, order_date)
""")
_shared_connection.sql("""
    CREATE TABLE products AS SELECT * FROM (VALUES
        (1, 'ノートPC',   120000, '電子機器'),
        (2, 'マウス',       2500, '電子機器'),
        (3, 'コーヒー豆',   1500, '食品'),
        (4, 'キーボード',  15000, '電子機器'),
        (5, 'モニター',    45000, '電子機器')
    ) t(id, name, price, category)
""")

api.db.connection.get_connection = lambda: _shared_connection
