from api.services.analyze_query.query_block.block_range_alias_finder import (
    find_block_ranges_with_alias,
)


def test_simple_select_has_one_range():
    query = "SELECT * FROM users"
    result = find_block_ranges_with_alias(query)
    assert len(result) == 1


def test_outer_range_spans_full_query():
    query = "SELECT * FROM users"
    result = find_block_ranges_with_alias(query)
    (start, end) = list(result.keys())[0]
    assert start == 0
    assert end == len(query)


def test_simple_select_has_no_alias():
    query = "SELECT * FROM users"
    result = find_block_ranges_with_alias(query)
    assert all(alias is None for alias in result.values())


def test_subquery_in_from_has_two_ranges():
    query = "SELECT * FROM (SELECT id FROM users) AS sub"
    result = find_block_ranges_with_alias(query)
    assert len(result) == 2


def test_subquery_alias_is_recorded():
    query = "SELECT * FROM (SELECT id FROM users) AS sub"
    result = find_block_ranges_with_alias(query)
    assert "sub" in result.values()


def test_two_sibling_subqueries_has_three_ranges():
    query = (
        "SELECT * FROM (SELECT id FROM users) AS u "
        "JOIN (SELECT id FROM products) AS p ON u.id = p.id"
    )
    result = find_block_ranges_with_alias(query)
    assert len(result) == 3


def test_nested_subquery_has_three_ranges():
    query = "SELECT * FROM (SELECT id FROM (SELECT id FROM users) AS inner) AS outer"
    result = find_block_ranges_with_alias(query)
    assert len(result) == 3


def test_find_cte_single():
    query = "WITH cte AS (SELECT id FROM users) SELECT * FROM cte"
    result = find_block_ranges_with_alias(query)
    assert "cte" in result.values()


def test_find_cte_multiple():
    query = (
        "WITH a AS (SELECT id FROM users), b AS (SELECT id FROM products) "
        "SELECT * FROM a JOIN b ON a.id = b.id"
    )
    result = find_block_ranges_with_alias(query)
    aliases = set(result.values())
    assert "a" in aliases
    assert "b" in aliases


def test_no_cte_has_no_named_alias():
    query = "SELECT * FROM users"
    result = find_block_ranges_with_alias(query)
    assert not any(alias is not None for alias in result.values())
