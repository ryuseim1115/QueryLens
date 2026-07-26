from typing import Any, NamedTuple

import duckdb

from infrastructure.duckdb.connection import get_connection

# プレビュー用途のため結果行数に上限を設ける。無制限にfetchall()すると、
# 行数変換(Pythonループ)がGILを握り続け、同一プロセスの他リクエストを
# ブロックしてしまうため（詳細はQueryLensの障害調査を参照）。
RESULT_ROW_LIMIT = 1000


class QueryResult(NamedTuple):
    records: list[dict[str, Any]]
    truncated: bool


def run_query(user_id: int, query: str) -> QueryResult:
    # cursor()でリクエストごとの専用セッションを作り、
    # 他リクエストのクエリ実行と競合しないようにする
    with get_connection(user_id).cursor() as connection:
        try:
            result = connection.sql(query)
            # 上限+1件だけ取得し、超過分の有無で切り詰めたかどうかを判定する
            rows = result.fetchmany(RESULT_ROW_LIMIT + 1)
            truncated = len(rows) > RESULT_ROW_LIMIT
            records = [
                dict(zip(result.columns, record)) for record in rows[:RESULT_ROW_LIMIT]
            ]
            return QueryResult(records=records, truncated=truncated)
        except duckdb.BinderException:
            # ブロック単体実行時に外側のテーブルエイリアスを解決できない場合
            # （相関サブクエリなど）に発生する。未対応であることが伝わるメッセージにする
            # （対応方針は#63で検討中）
            raise ValueError("相関サブクエリは未対応です。今後の対応をお待ちください。")
        except Exception as e:
            raise ValueError(f"クエリの実行に失敗しました: {e}")
