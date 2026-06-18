from api.db.connection import get_connection


def drop_table(file_name: str):
    table_name = file_name.removesuffix(".csv")
    connection = get_connection()
    connection.sql(f'DROP TABLE IF EXISTS "{table_name}"')
