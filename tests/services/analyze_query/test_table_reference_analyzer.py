from api.services.analyze_query.query_block.block_range_alias_finder import (
    find_block_ranges_with_alias,
)
from api.services.analyze_query.query_block.query_structure_analyzer import (
    build_query_blocks,
)
from api.services.analyze_query.table_reference.table_reference_analyzer import (
    analyze_table_references,
)


def _analyze(query: str):
    block_ranges_alias = find_block_ranges_with_alias(query)
    return build_query_blocks(query, block_ranges_alias)


def test_analyze_table_references_converts_to_tableinfo():
    from api.schemas.run_query import TableInfo

    query = "SELECT * FROM users"
    query_blocks = _analyze(query)
    result = analyze_table_references(query, query_blocks)
    outer = next(r for r in result if r.depth == 0)
    assert all(isinstance(t, TableInfo) for t in outer.table_references)


def test_analyze_table_references_table_name_is_recorded():
    query = "SELECT * FROM products"
    query_blocks = _analyze(query)
    result = analyze_table_references(query, query_blocks)
    assert any(t.table_name == "products" for t in result[0].table_references)


def test_analyze_table_references_links_cte_reference_to_its_block():
    query = "WITH cte AS (SELECT id FROM users) SELECT * FROM cte"
    query_blocks = _analyze(query)
    result = analyze_table_references(query, query_blocks)

    cte_block = next(r for r in result if r.parent_alias == "cte")
    outer_block = next(r for r in result if r.depth == 0)
    cte_reference = next(
        t for t in outer_block.table_references if t.table_name == "cte"
    )

    assert cte_reference.referenced_block_start_index == cte_block.start_index
    assert cte_reference.referenced_block_end_index == cte_block.end_index
