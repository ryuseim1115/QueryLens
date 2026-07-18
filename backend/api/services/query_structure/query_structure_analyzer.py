from api.schemas.run_query import (
    QueryBlockAnalyzeResult,
    QueryBlockAnalyzeResultList,
    TableInfo,
)
from api.services.query_structure.query_block_builder import QueryStructureBuilder


class QueryStructureAnalyzer:
    def __init__(self, query: str):
        self.query = query

    def execute(self) -> QueryBlockAnalyzeResultList:
        query_blocks = QueryStructureBuilder(self.query).execute()
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
