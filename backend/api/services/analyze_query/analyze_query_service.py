from api.schemas.run_query import QueryBlockAnalyzeResultList
from api.services.analyze_query.query_block.block_range_alias_finder import (
    find_block_ranges_with_alias,
)
from api.services.analyze_query.query_block.query_structure_analyzer import (
    build_query_blocks,
)
from api.services.analyze_query.query_block.sort_query_blocks import (
    sort_query_blocks_by_depth_desc,
)
from api.services.analyze_query.table_reference.table_reference_analyzer import (
    analyze_table_references,
)
from api.validators.query_validator import QueryValidator


def analyze_query(
    user_id: int, database_type: str, query: str
) -> QueryBlockAnalyzeResultList:
    QueryValidator(database_type, query, user_id).validate()
    # クエリをブロックに分解し、それぞれの範囲・エイリアスを特定
    block_ranges_alias = find_block_ranges_with_alias(query)
    query_blocks = build_query_blocks(query, block_ranges_alias)
    query_blocks = analyze_table_references(query, query_blocks)
    query_blocks = sort_query_blocks_by_depth_desc(query_blocks)
    return query_blocks
