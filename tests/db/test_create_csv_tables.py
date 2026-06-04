from api.db.connection import get_connection


def test_all_tables_exist():
    conn = get_connection()
    tables = {row[0] for row in conn.sql("SHOW TABLES").fetchall()}
    expected = {
        "users",
        "products",
        "orders",
        "reviews",
        "stores",
        "inventory",
        "shipping",
        "campaigns",
        "employees",
        "point_history",
    }
    assert expected.issubset(tables)


def test_users_row_count():
    conn = get_connection()
    count = conn.sql("SELECT COUNT(*) FROM users").fetchone()[0]
    assert count == 20


def test_products_row_count():
    conn = get_connection()
    count = conn.sql("SELECT COUNT(*) FROM products").fetchone()[0]
    assert count == 20


def test_orders_row_count():
    conn = get_connection()
    count = conn.sql("SELECT COUNT(*) FROM orders").fetchone()[0]
    assert count == 20


def test_users_columns():
    conn = get_connection()
    result = conn.sql("SELECT * FROM users LIMIT 0")
    assert set(result.columns) == {"id", "name", "email", "age"}


def test_products_columns():
    conn = get_connection()
    result = conn.sql("SELECT * FROM products LIMIT 0")
    assert set(result.columns) == {"id", "name", "price", "category"}


def test_orders_columns():
    conn = get_connection()
    result = conn.sql("SELECT * FROM orders LIMIT 0")
    assert set(result.columns) == {"id", "user_id", "product_id", "amount", "order_date"}


def test_users_first_row():
    conn = get_connection()
    row = conn.sql("SELECT name, email, age FROM users WHERE id = 1").fetchone()
    assert row == ("山田太郎", "yamada@example.com", 28)


def test_products_food_category_count():
    conn = get_connection()
    count = conn.sql("SELECT COUNT(*) FROM products WHERE category = '食品'").fetchone()[0]
    assert count == 5
