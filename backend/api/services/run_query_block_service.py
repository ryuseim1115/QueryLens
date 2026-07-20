from api.schemas.run_query import QueryBlockAnalyzeResult
from api.services.query_structure.query_block_runner import QueryBlockRunner
from api.services.query_structure.query_structure_analyzer import (
    QueryStructureAnalyzer,
)
from api.validators.query_validator import QueryValidator


def run_query_block(
    user_id: int, database_type: str, query: str, start_index: int
) -> QueryBlockAnalyzeResult:
    QueryValidator(database_type, query, user_id).validate()
    query_blocks = QueryStructureAnalyzer(query).execute()

    query_block = next(
        (qb for qb in query_blocks if qb.start_index == start_index), None
    )
    if query_block is None:
        raise ValueError("指定されたクエリブロックが見つかりません")

    return QueryBlockRunner(user_id, [query_block]).execute()[0]