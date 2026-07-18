import os

from infrastructure.disk.build_csv_path import build_csv_path


def delete_disk_file(user_id: int, file_name: str) -> None:
    csv_path = build_csv_path(user_id, file_name)
    if os.path.exists(csv_path):
        os.remove(csv_path)
