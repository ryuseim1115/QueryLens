import os

import duckdb

CSV_FILES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "csv_files")
)

FILE_NAME_TABLE_MAP = {
    "test1.csv": "users",
    "test2.csv": "orders",
    "test3.csv": "products",
}

# テスト全体で共有するインメモリ接続を作成し、テーブルをロードする
_shared_connection = duckdb.connect()
for _file_name, _table_name in FILE_NAME_TABLE_MAP.items():
    _path = os.path.join(CSV_FILES_DIR, _file_name)
    _shared_connection.sql(
        f"CREATE OR REPLACE TABLE \"{_table_name}\" AS SELECT * FROM '{_path}'"
    )

# get_connection() を共有接続を返す関数で差し替える
import api.db.connection  # noqa: E402

api.db.connection.get_connection = lambda: _shared_connection
