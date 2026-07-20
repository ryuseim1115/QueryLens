from api.schemas.run_query import QueryBlockAnalyzeResultList
from api.services.query_structure.query_structure_analyzer import (
    QueryStructureAnalyzer,
)
from api.services.query_structure.sort_query_blocks import SortQueryBlocksByDepthDesc
from api.validators.query_validator import QueryValidator


def run_query(
    user_id: int, database_type: str, query: str
) -> QueryBlockAnalyzeResultList:
    QueryValidator(database_type, query, user_id).validate()
    query_blocks = QueryStructureAnalyzer(query).execute()
    query_blocks = SortQueryBlocksByDepthDesc(query_blocks).execute()
    return query_blocks
