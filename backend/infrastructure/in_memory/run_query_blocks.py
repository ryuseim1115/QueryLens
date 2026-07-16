from api.schemas.run_query import QueryBlockAnalyzeResultList

from infrastructure.in_memory.connection import get_connection, get_user_schema


def run_query_blocks(
    user_id: int,
    query_blocks: QueryBlockAnalyzeResultList,
) -> QueryBlockAnalyzeResultList:
    schema = get_user_schema(user_id)
    # cursor()で専用セッションを作り、USEで切り替えたデフォルトスキーマが
    # 他リクエストのクエリ実行と競合しないようにする
    connection = get_connection().cursor()
    connection.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
    connection.execute(f'USE "{schema}"')
    for query_block in query_blocks:
        try:
            result = connection.sql(query_block.query)
            query_block.result = [
                dict(zip(result.columns, record)) for record in result.fetchall()
            ]
        except Exception as e:
            raise ValueError(f"クエリブロックの実行に失敗しました: {e}")
    return query_blocks
