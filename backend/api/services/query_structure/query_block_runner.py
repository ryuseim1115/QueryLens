from api.schemas.run_query import QueryBlockAnalyzeResultList
from infrastructure.duckdb.run_query_blocks import run_query_blocks


class QueryBlockRunner:
    def __init__(self, user_id: int, query_blocks: QueryBlockAnalyzeResultList):
        self.user_id = user_id
        self.query_blocks = query_blocks

    def execute(self) -> QueryBlockAnalyzeResultList:
        self.query_blocks = run_query_blocks(self.user_id, self.query_blocks)
        return self.query_blocks
