from api.schemas.run_query import QueryBlockAnalyzeResultList
from api.services.query_structure.query_structure_analyzer import (
    analyze_query_structure,
    resolve_table_references,
)
from api.services.query_structure.sort_query_blocks import (
    sort_query_blocks_by_depth_desc,
)
from api.validators.query_validator import QueryValidator


def analyze_query(
    user_id: int, database_type: str, query: str
) -> QueryBlockAnalyzeResultList:
    QueryValidator(database_type, query, user_id).validate()
    query_blocks = analyze_query_structure(query)
    query_blocks = resolve_table_references(query_blocks)
    query_blocks = sort_query_blocks_by_depth_desc(query_blocks)
    return query_blocks
