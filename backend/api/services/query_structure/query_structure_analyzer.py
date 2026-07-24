from api.schemas.run_query import (
    QueryBlockAnalyzeResult,
    QueryBlockAnalyzeResultList,
    TableInfo,
)
from api.services.query_structure.query_block_builder import build_query_blocks


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
                TableInfo(name=name, alias=alias)
                for name, alias in query_block.tables_name_alias
            ],
            parent_alias=query_block.parent_alias,
            result=[],
        )
        for query_block in query_blocks
    ]
