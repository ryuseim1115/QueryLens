from infrastructure.disk.delete_disk_file import delete_disk_file
from infrastructure.duckdb.drop_table import drop_table


def purge_file(user_id: int, file_name: str) -> None:
    drop_table(user_id, file_name)
    delete_disk_file(user_id, file_name)
