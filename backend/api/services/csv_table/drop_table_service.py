from infrastructure.duckdb.drop_table import drop_table as drop_table_disk_csv


def drop_table(user_id: int, file_name: str) -> None:
    drop_table_disk_csv(user_id, file_name)
