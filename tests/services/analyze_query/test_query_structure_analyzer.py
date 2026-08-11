from api.services.analyze_query.query_block.block_range_alias_finder import (
    find_block_ranges_with_alias,
)
from api.services.analyze_query.query_block.query_structure_analyzer import (
    build_query_blocks,
)


def _analyze(query: str):
    block_ranges_alias = find_block_ranges_with_alias(query)
    return build_query_blocks(query, block_ranges_alias)


def test_simple_query_has_one_result():
    result = _analyze("SELECT * FROM users")
    assert len(result) == 1


def test_simple_query_depth_is_zero():
    result = _analyze("SELECT * FROM users")
    assert result[0].depth == 0


def test_simple_query_text_matches():
    query = "SELECT * FROM users"
    result = _analyze(query)
    assert result[0].query == query


def test_subquery_depths_include_zero_and_one():
    query = "SELECT * FROM (SELECT id FROM products) AS sub"
    result = _analyze(query)
    depths = {r.depth for r in result}
    assert 0 in depths
    assert 1 in depths


def test_cte_query_has_cte_alias():
    query = "WITH cte AS (SELECT id FROM users) SELECT * FROM cte"
    result = _analyze(query)
    assert any(r.parent_alias == "cte" for r in result)


def test_nested_subquery_depths_include_zero_one_two():
    query = "SELECT * FROM (SELECT id FROM (SELECT id FROM users) AS inner) AS outer"
    result = _analyze(query)
    depths = sorted(r.depth for r in result)
    assert depths == [0, 1, 2]


def test_multiple_cte_aliases():
    query = (
        "WITH a AS (SELECT id FROM users), b AS (SELECT id FROM products) "
        "SELECT * FROM a JOIN b ON a.id = b.id"
    )
    result = _analyze(query)
    aliases = {r.parent_alias for r in result}
    assert "a" in aliases
    assert "b" in aliases
