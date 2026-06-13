from api.services.analyze_subquery.query_structure_analyzer import QueryStructureAnalyzer


def test_simple_query_has_one_result():
    result = QueryStructureAnalyzer("SELECT * FROM users").execute()
    assert len(result) == 1


def test_simple_query_depth_is_zero():
    result = QueryStructureAnalyzer("SELECT * FROM users").execute()
    assert result[0].depth == 0


def test_simple_query_text_matches():
    query = "SELECT * FROM users"
    result = QueryStructureAnalyzer(query).execute()
    assert result[0].query == query


def test_subquery_depths_include_zero_and_one():
    query = "SELECT * FROM (SELECT id FROM products) AS sub"
    result = QueryStructureAnalyzer(query).execute()
    depths = {r.depth for r in result}
    assert 0 in depths
    assert 1 in depths


def test_cte_query_has_cte_alias():
    query = "WITH cte AS (SELECT id FROM users) SELECT * FROM cte"
    result = QueryStructureAnalyzer(query).execute()
    assert any(r.parent_alias == "cte" for r in result)


def test_result_contains_tableinfo_objects():
    from api.schemas.run_query import TableInfo

    result = QueryStructureAnalyzer("SELECT * FROM users").execute()
    outer = next(r for r in result if r.depth == 0)
    assert all(isinstance(t, TableInfo) for t in outer.tables_name_alias)


def test_result_items_have_empty_result_list():
    result = QueryStructureAnalyzer("SELECT * FROM users").execute()
    assert all(r.result == [] for r in result)
