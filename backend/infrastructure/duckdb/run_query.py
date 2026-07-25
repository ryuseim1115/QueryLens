from typing import Any

import duckdb

from infrastructure.duckdb.connection import get_connection


def run_query(user_id: int, query: str) -> list[dict[str, Any]]:
    # cursor()でリクエストごとの専用セッションを作り、
    # 他リクエストのクエリ実行と競合しないようにする
    with get_connection(user_id).cursor() as connection:
        try:
            result = connection.sql(query)
            return [dict(zip(result.columns, record)) for record in result.fetchall()]
        except duckdb.BinderException:
            # ブロック単体実行時に外側のテーブルエイリアスを解決できない場合
            # （相関サブクエリなど）に発生する。未対応であることが伝わるメッセージにする
            # （対応方針は#63で検討中）
            raise ValueError("相関サブクエリは未対応です。今後の対応をお待ちください。")
        except Exception as e:
            raise ValueError(f"クエリの実行に失敗しました: {e}")
