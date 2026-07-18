from infrastructure.in_memory.connection import get_connection, get_user_schema


def drop_table(user_id: int, file_name: str):
    schema = get_user_schema(user_id)
    table_name = file_name.removesuffix(".csv")
    connection = get_connection().cursor()
    connection.sql(f'DROP TABLE IF EXISTS "{schema}"."{table_name}"')
