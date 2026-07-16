from infrastructure.in_memory.connection import get_connection, get_user_schema


def get_in_memory_table_names(user_id: int) -> set[str]:
    schema = get_user_schema(user_id)
    connection = get_connection().cursor()
    rows = connection.execute(
        "SELECT table_name FROM duckdb_tables() WHERE schema_name = ?", [schema]
    ).fetchall()
    return {row[0] for row in rows}
