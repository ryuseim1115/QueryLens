from typing import Any

from infrastructure.duckdb.connection import get_connection


def run_query(user_id: int, query: str) -> list[dict[str, Any]]:
    # cursor()でリクエストごとの専用セッションを作り、
    # 他リクエストのクエリ実行と競合しないようにする
    with get_connection(user_id).cursor() as connection:
        try:
            result = connection.sql(query)
            return [dict(zip(result.columns, record)) for record in result.fetchall()]
        except Exception as e:
            raise ValueError(f"クエリの実行に失敗しました: {e}")
