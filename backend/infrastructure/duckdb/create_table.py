from infrastructure.disk.build_csv_path import build_csv_path
from infrastructure.duckdb.connection import get_connection


def create_table(user_id: int, file_name: str):
    csv_path = build_csv_path(user_id, file_name)
    table_name = file_name.removesuffix(".csv")
    connection = get_connection(user_id).cursor()
    sql = f"CREATE OR REPLACE TABLE \"{table_name}\" AS SELECT * FROM '{csv_path}'"
    connection.sql(sql)
