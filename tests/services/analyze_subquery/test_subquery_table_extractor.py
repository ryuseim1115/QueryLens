from api.services.analyze_subquery.subquery_table_extractor import extract_tables_with_alias


def test_single_table_no_alias():
    result = extract_tables_with_alias("SELECT * FROM users")
    assert len(result) == 1
    assert result[0][0] == "users"
    assert result[0][1] is None


def test_single_table_with_alias():
    result = extract_tables_with_alias("SELECT u.id FROM users AS u")
    assert len(result) == 1
    assert result[0][0] == "users"
    assert result[0][1] == "u"


def test_parens_wrapped_query():
    result = extract_tables_with_alias("(SELECT * FROM products AS p)")
    assert any(t[0] == "products" for t in result)


def test_join_extracts_both_tables():
    result = extract_tables_with_alias(
        "SELECT * FROM users JOIN orders ON users.id = orders.user_id"
    )
    names = [t[0] for t in result]
    assert "users" in names
    assert "orders" in names


def test_left_join_with_aliases():
    result = extract_tables_with_alias(
        "SELECT u.name, o.amount FROM users AS u LEFT JOIN orders AS o ON u.id = o.user_id"
    )
    assert any(t == ("users", "u") for t in result)
    assert any(t == ("orders", "o") for t in result)


def test_subquery_in_from_has_none_name():
    result = extract_tables_with_alias(
        "SELECT * FROM (SELECT id FROM users) AS sub"
    )
    assert any(t[1] == "sub" for t in result)
    subquery_entry = next(t for t in result if t[1] == "sub")
    assert subquery_entry[0] is None


def test_empty_on_invalid_query():
    result = extract_tables_with_alias("NOT VALID SQL")
    assert isinstance(result, list)
