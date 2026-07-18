import sqlglot
from api.services.query_structure.range_finder import (
    find_cte_ranges,
    find_subquery_ranges,
)


def _tokenize(query: str):
    return sqlglot.tokens.Tokenizer().tokenize(query)


def test_simple_select_has_one_range():
    query = "SELECT * FROM users"
    result = find_subquery_ranges(query, _tokenize(query))
    assert len(result) == 1


def test_outer_range_spans_full_query():
    query = "SELECT * FROM users"
    tokens = _tokenize(query)
    result = find_subquery_ranges(query, tokens)
    (start, end) = list(result.keys())[0]
    assert start == tokens[0].start
    assert end == tokens[-1].end + 1


def test_subquery_in_from_has_two_ranges():
    query = "SELECT * FROM (SELECT id FROM users) AS sub"
    result = find_subquery_ranges(query, _tokenize(query))
    assert len(result) == 2


def test_two_sibling_subqueries_has_three_ranges():
    query = (
        "SELECT * FROM (SELECT id FROM users) AS u "
        "JOIN (SELECT id FROM products) AS p ON u.id = p.id"
    )
    result = find_subquery_ranges(query, _tokenize(query))
    assert len(result) == 3


def test_nested_subquery_has_three_ranges():
    query = "SELECT * FROM (SELECT id FROM (SELECT id FROM users) AS inner) AS outer"
    result = find_subquery_ranges(query, _tokenize(query))
    assert len(result) == 3


def test_find_cte_single():
    query = "WITH cte AS (SELECT id FROM users) SELECT * FROM cte"
    result = find_cte_ranges(_tokenize(query))
    assert len(result) == 1
    assert list(result.values())[0] == "cte"


def test_find_cte_multiple():
    query = (
        "WITH a AS (SELECT id FROM users), b AS (SELECT id FROM products) "
        "SELECT * FROM a JOIN b ON a.id = b.id"
    )
    result = find_cte_ranges(_tokenize(query))
    assert len(result) == 2
    assert set(result.values()) == {"a", "b"}


def test_no_cte_returns_empty():
    query = "SELECT * FROM users"
    result = find_cte_ranges(_tokenize(query))
    assert result == {}
