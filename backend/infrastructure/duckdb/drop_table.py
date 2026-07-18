from infrastructure.duckdb.connection import get_connection


def drop_table(user_id: int, file_name: str):
    table_name = file_name.removesuffix(".csv")
    connection = get_connection(user_id).cursor()
    connection.sql(f'DROP TABLE IF EXISTS "{table_name}"')
