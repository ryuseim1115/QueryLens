from api.services.query_structure.query_structure_analyzer import (
    analyze_query_structure,
)


def test_simple_query_has_one_result():
    result = analyze_query_structure("SELECT * FROM users")
    assert len(result) == 1


def test_simple_query_depth_is_zero():
    result = analyze_query_structure("SELECT * FROM users")
    assert result[0].depth == 0


def test_simple_query_text_matches():
    query = "SELECT * FROM users"
    result = analyze_query_structure(query)
    assert result[0].query == query


def test_subquery_depths_include_zero_and_one():
    query = "SELECT * FROM (SELECT id FROM products) AS sub"
    result = analyze_query_structure(query)
    depths = {r.depth for r in result}
    assert 0 in depths
    assert 1 in depths


def test_cte_query_has_cte_alias():
    query = "WITH cte AS (SELECT id FROM users) SELECT * FROM cte"
    result = analyze_query_structure(query)
    assert any(r.parent_alias == "cte" for r in result)


def test_result_contains_tableinfo_objects():
    from api.schemas.run_query import TableInfo

    result = analyze_query_structure("SELECT * FROM users")
    outer = next(r for r in result if r.depth == 0)
    assert all(isinstance(t, TableInfo) for t in outer.tables_name_alias)


def test_result_items_have_empty_result_list():
    result = analyze_query_structure("SELECT * FROM users")
    assert all(r.result == [] for r in result)
