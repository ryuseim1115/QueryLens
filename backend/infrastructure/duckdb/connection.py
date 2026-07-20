import os
import threading

import duckdb
from config import DUCKDB_DIR

_connections: dict[int, duckdb.DuckDBPyconnection] = {}
_init_lock = threading.Lock()


# ユーザーごとに別々のDuckDBファイルを持たせることで、あるユーザーの
# テーブル作成が他ユーザーのクエリ実行と同じファイルを取り合わないようにしている。
def get_connection(user_id: int) -> duckdb.DuckDBPyconnection:
    connection = _connections.get(user_id)
    if connection is None:
        # 既存のユーザーの接続取得ではロックを取らずに済むよう、
        # 先にロックなしで確認してから初期化用のロックに入る。
        with _init_lock:
            # ロック待ちの間に他スレッドが作成済みの場合があるため再確認し、
            # 同じユーザーの接続が二重に作られてリークするのを防ぐ。
            connection = _connections.get(user_id)
            if connection is None:
                os.makedirs(DUCKDB_DIR, exist_ok=True)
                path = os.path.join(DUCKDB_DIR, f"{user_id}.duckdb")
                connection = duckdb.connect(path)
                _connections[user_id] = connection
    return connection
