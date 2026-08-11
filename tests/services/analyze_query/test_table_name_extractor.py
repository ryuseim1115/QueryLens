from api.services.analyze_query.table_reference.table_name_extractor import (
    extract_table_names_with_alias,
)


def _extract(query: str):
    return extract_table_names_with_alias(query)


def test_single_table_no_alias():
    result = _extract("SELECT * FROM users")
    assert len(result) == 1
    assert result[0][0] == "users"
    assert result[0][1] is None


def test_single_table_with_alias():
    result = _extract("SELECT u.id FROM users AS u")
    assert len(result) == 1
    assert result[0][0] == "users"
    assert result[0][1] == "u"


def test_parens_wrapped_query():
    result = _extract("(SELECT * FROM products AS p)")
    assert any(t[0] == "products" for t in result)


def test_join_extracts_both_tables():
    result = _extract("SELECT * FROM users JOIN orders ON users.id = orders.user_id")
    names = [t[0] for t in result]
    assert "users" in names
    assert "orders" in names


def test_left_join_with_aliases():
    result = _extract(
        "SELECT u.name, o.amount FROM users AS u "
        "LEFT JOIN orders AS o ON u.id = o.user_id"
    )
    assert any(t[:2] == ("users", "u") for t in result)
    assert any(t[:2] == ("orders", "o") for t in result)


def test_subquery_in_from_has_none_name():
    result = _extract("SELECT * FROM (SELECT id FROM users) AS sub")
    assert any(t[1] == "sub" for t in result)
    subquery_entry = next(t for t in result if t[1] == "sub")
    assert subquery_entry[0] is None


def test_values_clause_in_from_is_excluded():
    # FROM句がexp.Table/exp.Subqueryのどちらでもないケース(VALUES句)
    result = _extract("SELECT * FROM (VALUES (1,2)) AS t(a,b)")
    assert result == []


def test_table_position_points_to_table_name_only():
    query = "SELECT * FROM small_products"
    result = _extract(query)
    start, end = result[0][2]
    assert query[start:end] == "small_products"


def test_aliased_table_position_points_to_name_not_alias():
    query = "SELECT * FROM users AS u"
    result = _extract(query)
    start, end = result[0][2]
    assert query[start:end] == "users"


def test_subquery_position_points_to_alias():
    query = "SELECT * FROM (SELECT id FROM users) AS sub"
    result = _extract(query)
    subquery_entry = next(t for t in result if t[1] == "sub")
    start, end = subquery_entry[2]
    assert query[start:end] == "sub"


def test_select_list_scalar_subquery_is_extracted():
    query = "SELECT u.id, (SELECT COUNT(*) FROM orders) AS order_count FROM users AS u"
    result = _extract(query)
    assert any(t[:2] == (None, "order_count") for t in result)


def test_select_list_scalar_subquery_position_points_to_alias():
    query = "SELECT (SELECT COUNT(*) FROM orders) AS order_count FROM users"
    result = _extract(query)
    entry = next(t for t in result if t[1] == "order_count")
    start, end = entry[2]
    assert query[start:end] == "order_count"


def test_select_list_multiple_scalar_subqueries_are_extracted():
    query = (
        "SELECT "
        "(SELECT COUNT(*) FROM orders AS o WHERE o.user_id = u.id) AS order_count, "
        "(SELECT COALESCE(SUM(o.amount), 0) FROM orders AS o WHERE o.user_id = u.id) "
        "AS total_amount "
        "FROM users AS u"
    )
    result = _extract(query)
    aliases = [t[1] for t in result]
    assert "order_count" in aliases
    assert "total_amount" in aliases


def test_select_list_plain_column_alias_is_not_extracted():
    result = _extract("SELECT u.id AS user_id FROM users AS u")
    assert all(t[1] != "user_id" for t in result)


def test_select_list_subquery_buried_in_expression_is_not_extracted():
    # サブクエリが式の一部に埋もれているケース（対象外の既知の制約）
    result = _extract("SELECT (SELECT COUNT(*) FROM orders) + 1 AS total FROM users")
    assert all(t[1] != "total" for t in result)


# --- ここから、クエリ全体を1回でパースするようになったことで
#     ブロックの深さに関わらずまとめて抽出されることを確認するテスト ---


def test_nested_subquery_tables_are_all_extracted_in_one_call():
    # ブロックごとに再パースしなくなったため、ネストしたサブクエリの中の
    # テーブルも1回の呼び出しで一緒に抽出される
    query = "SELECT * FROM (SELECT id FROM (SELECT id FROM users) AS inner) AS outer"
    result = _extract(query)
    names_and_aliases = [t[:2] for t in result]
    assert ("users", None) in names_and_aliases
    assert (None, "inner") in names_and_aliases
    assert (None, "outer") in names_and_aliases


def test_cte_body_tables_are_extracted():
    query = "WITH cte AS (SELECT id FROM users) SELECT * FROM cte"
    result = _extract(query)
    names = [t[0] for t in result]
    assert "users" in names
    assert "cte" in names


def test_scalar_subquery_body_tables_are_also_extracted():
    # スカラーサブクエリのエイリアス自体だけでなく、その中身が参照する
    # テーブルもまとめて抽出される（どのブロックに属するかの判定はしない）
    query = "SELECT (SELECT COUNT(*) FROM orders) AS order_count FROM users"
    result = _extract(query)
    names = [t[0] for t in result]
    assert "orders" in names
    assert "users" in names
