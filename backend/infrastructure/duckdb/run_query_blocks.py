from api.schemas.run_query import QueryBlockAnalyzeResultList

from infrastructure.duckdb.connection import get_connection


def run_query_blocks(
    user_id: int,
    query_blocks: QueryBlockAnalyzeResultList,
) -> QueryBlockAnalyzeResultList:
    # cursor()でリクエストごとの専用セッションを作り、他リクエストのクエリ実行と競合しないようにする
    with get_connection(user_id).cursor() as connection:
        for query_block in query_blocks:
            try:
                result = connection.sql(query_block.query)
                query_block.result = [
                    dict(zip(result.columns, record)) for record in result.fetchall()
                ]
            except Exception as e:
                raise ValueError(f"クエリブロックの実行に失敗しました: {e}")
    return query_blocks
