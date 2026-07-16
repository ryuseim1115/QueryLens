import threading

import duckdb
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_ID, REGION_NAME

connection = None
_init_lock = threading.Lock()


# DuckDBのconnectionオブジェクト自体はスレッドセーフではないため、
# 複数リクエストから同時にSQLを実行させると内部のpending query stateが
# 壊れてしまう(Issue #81)。呼び出し側は必ずこの関数が返すconnectionを
# 直接使わず、connection.cursor()で取得した専用セッション経由で
# SQLを実行すること。
def get_connection() -> duckdb.DuckDBPyconnection:
    global connection
    if connection is None:
        with _init_lock:
            if connection is None:
                connection = duckdb.connect()
                connection.execute("INSTALL httpfs; LOAD httpfs;")
                connection.execute(
                    f""" SET s3_region='{REGION_NAME}';
                    SET s3_access_key_id='{AWS_ACCESS_KEY_ID}';
                    SET s3_secret_access_key='{AWS_SECRET_ACCESS_KEY_ID}';"""
                )
    return connection


def get_user_schema(user_id: int) -> str:
    return f"user_{user_id}"
