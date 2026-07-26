from api.schemas.run_query import (
    QueryBlockAnalyzeResult,
    QueryBlockAnalyzeResultList,
    TableInfo,
)
from api.services.query_structure.query_block_builder import (
    QueryBlock,
    build_query_blocks,
)
from api.services.query_structure.table_position_finder import find_table_position


# 構造解析自体はbuild_query_blocksが担い、ここでは内部表現QueryBlockのリストを
# API応答用スキーマQueryBlockAnalyzeResultのリストに変換する
def analyze_query_structure(query: str) -> QueryBlockAnalyzeResultList:
    query_blocks = build_query_blocks(query)
    return [
        QueryBlockAnalyzeResult(
            start_index=query_block.start_index,
            end_index=query_block.end_index,
            query=query_block.query,
            depth=query_block.depth,
            tables_name_alias=[
                _build_table_info(table_name, alias, position, query_blocks)
                for table_name, alias, position in query_block.tables_name_alias
            ],
            parent_alias=query_block.parent_alias,
            result=[],
        )
        for query_block in query_blocks
    ]


def _build_table_info(
    table_name: str | None,
    alias: str | None,
    position: tuple[int, int] | None,
    query_blocks: list[QueryBlock],
) -> TableInfo:
    referenced_block_position = find_table_position(table_name, alias, query_blocks)
    return TableInfo(
        table_name=table_name,
        alias=alias,
        start_index=position[0] if position else None,
        end_index=position[1] if position else None,
        referenced_block_start_index=(
            referenced_block_position[0] if referenced_block_position else None
        ),
        referenced_block_end_index=(
            referenced_block_position[1] if referenced_block_position else None
        ),
    )
