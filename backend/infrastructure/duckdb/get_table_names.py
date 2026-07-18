from infrastructure.duckdb.connection import get_connection


def get_table_names(user_id: int) -> set[str]:
    connection = get_connection(user_id).cursor()
    rows = connection.execute("SELECT table_name FROM duckdb_tables()").fetchall()
    return {row[0] for row in rows}
