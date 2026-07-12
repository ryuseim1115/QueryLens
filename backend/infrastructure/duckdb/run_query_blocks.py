from api.schemas.run_query import QueryBlockAnalyzeResultList

from infrastructure.duckdb.connection import get_connection


def run_query_blocks(
    query_blocks: QueryBlockAnalyzeResultList,
) -> QueryBlockAnalyzeResultList:
    connection = get_connection()
    for query_block in query_blocks:
        try:
            result = connection.sql(query_block.query)
            query_block.result = [
                dict(zip(result.columns, record)) for record in result.fetchall()
            ]
        except Exception as e:
            raise ValueError(f"クエリブロックの実行に失敗しました: {e}")
    return query_blocks
