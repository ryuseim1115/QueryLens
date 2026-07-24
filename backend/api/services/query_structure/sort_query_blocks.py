from api.schemas.run_query import QueryBlockAnalyzeResultList


def sort_query_blocks_by_depth_desc(
    query_blocks: QueryBlockAnalyzeResultList,
) -> QueryBlockAnalyzeResultList:
    return sorted(query_blocks, key=lambda qb: qb.depth, reverse=True)
