from api.services.query_structure.query_structure_analyzer import (
    analyze_query_structure,
    resolve_table_references,
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


def test_simple_query_table_name_is_recorded():
    result = analyze_query_structure("SELECT * FROM products")
    table_names = [table_name for table_name, _, _ in result[0].tables_name_alias]
    assert "products" in table_names


def test_nested_subquery_depths_include_zero_one_two():
    query = "SELECT * FROM (SELECT id FROM (SELECT id FROM users) AS inner) AS outer"
    result = analyze_query_structure(query)
    depths = sorted(r.depth for r in result)
    assert depths == [0, 1, 2]


def test_multiple_cte_aliases():
    query = (
        "WITH a AS (SELECT id FROM users), b AS (SELECT id FROM products) "
        "SELECT * FROM a JOIN b ON a.id = b.id"
    )
    result = analyze_query_structure(query)
    aliases = {r.parent_alias for r in result}
    assert "a" in aliases
    assert "b" in aliases


def test_resolve_table_references_converts_to_tableinfo():
    from api.schemas.run_query import TableInfo

    query_blocks = analyze_query_structure("SELECT * FROM users")
    result = resolve_table_references(query_blocks)
    outer = next(r for r in result if r.depth == 0)
    assert all(isinstance(t, TableInfo) for t in outer.tables_name_alias)


def test_resolve_table_references_result_is_empty():
    query_blocks = analyze_query_structure("SELECT * FROM users")
    result = resolve_table_references(query_blocks)
    assert all(r.result == [] for r in result)


def test_resolve_table_references_table_name_is_recorded():
    query_blocks = analyze_query_structure("SELECT * FROM products")
    result = resolve_table_references(query_blocks)
    assert any(t.table_name == "products" for t in result[0].tables_name_alias)


def test_resolve_table_references_links_cte_reference_to_its_block():
    query = "WITH cte AS (SELECT id FROM users) SELECT * FROM cte"
    query_blocks = analyze_query_structure(query)
    result = resolve_table_references(query_blocks)

    cte_block = next(r for r in result if r.parent_alias == "cte")
    outer_block = next(r for r in result if r.depth == 0)
    cte_reference = next(t for t in outer_block.tables_name_alias if t.table_name == "cte")

    assert cte_reference.referenced_block_start_index == cte_block.start_index
    assert cte_reference.referenced_block_end_index == cte_block.end_index
