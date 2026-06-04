from api.services.analyze_subquery.subquery_builder import AnalyzeSubquery


def test_simple_query_yields_one_subquery():
    result = AnalyzeSubquery("SELECT * FROM users").execute()
    assert len(result) == 1
    assert result[0].depth == 0


def test_simple_query_has_correct_table():
    result = AnalyzeSubquery("SELECT * FROM products").execute()
    assert len(result) == 1
    assert any(t[0] == "products" for t in result[0].tables_name_alias)


def test_subquery_in_from_yields_two():
    query = "SELECT * FROM (SELECT id FROM users) AS sub"
    result = AnalyzeSubquery(query).execute()
    assert len(result) == 2
    depths = {s.depth for s in result}
    assert depths == {0, 1}


def test_subquery_alias_is_recorded():
    query = "SELECT * FROM (SELECT id FROM users) AS sub"
    result = AnalyzeSubquery(query).execute()
    aliases = [s.parent_alias for s in result]
    assert "sub" in aliases


def test_nested_subquery_yields_three():
    query = "SELECT * FROM (SELECT id FROM (SELECT id FROM users) AS inner) AS outer"
    result = AnalyzeSubquery(query).execute()
    assert len(result) == 3
    depths = sorted(s.depth for s in result)
    assert depths == [0, 1, 2]


def test_cte_yields_at_least_two():
    query = "WITH cte AS (SELECT id FROM users) SELECT * FROM cte"
    result = AnalyzeSubquery(query).execute()
    assert len(result) >= 2


def test_cte_parent_alias_is_set():
    query = "WITH cte AS (SELECT id FROM users) SELECT * FROM cte"
    result = AnalyzeSubquery(query).execute()
    assert any(s.parent_alias == "cte" for s in result)


def test_multiple_cte_aliases():
    query = (
        "WITH a AS (SELECT id FROM users), b AS (SELECT id FROM products) "
        "SELECT * FROM a JOIN b ON a.id = b.id"
    )
    result = AnalyzeSubquery(query).execute()
    aliases = {s.parent_alias for s in result}
    assert "a" in aliases
    assert "b" in aliases
