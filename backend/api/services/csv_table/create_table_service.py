import duckdb
from infrastructure.duckdb.create_table import create_table as create_table_disk_csv


def create_table(user_id: int, file_name: str) -> None:
    try:
        create_table_disk_csv(user_id, file_name)
    except duckdb.Error as e:
        raise ValueError(str(e))
