import os
import threading

import duckdb
from config import DUCKDB_DIR

_connections: dict[int, duckdb.DuckDBPyconnection] = {}
_init_lock = threading.Lock()


# DuckDBのconnectionオブジェクト自体はスレッドセーフではないため、
# 複数リクエストから同時にSQLを実行させると内部のpending query stateが
# 壊れてしまう(Issue #81)。呼び出し側は必ずこの関数が返すconnectionを
# 直接使わず、connection.cursor()で取得した専用セッション経由で
# SQLを実行すること。
#
# ユーザーごとに別々のDuckDBファイルを持たせることで、あるユーザーの
# テーブル作成が他ユーザーのクエリ実行と同じファイルを取り合わないようにしている。
def get_connection(user_id: int) -> duckdb.DuckDBPyconnection:
    connection = _connections.get(user_id)
    if connection is None:
        with _init_lock:
            connection = _connections.get(user_id)
            if connection is None:
                os.makedirs(DUCKDB_DIR, exist_ok=True)
                path = os.path.join(DUCKDB_DIR, f"{user_id}.duckdb")
                connection = duckdb.connect(path)
                _connections[user_id] = connection
    return connection
