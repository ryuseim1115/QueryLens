from api.schemas.run_query import QueryBlockAnalyzeResultList


class SortQueryBlocksByDepthDesc:
    def __init__(self, query_blocks: QueryBlockAnalyzeResultList):
        self.query_blocks = query_blocks

    def execute(self) -> QueryBlockAnalyzeResultList:
        sorted_query_blocks = sorted(
            self.query_blocks, key=lambda s: s.depth, reverse=True
        )
        return sorted_query_blocks
