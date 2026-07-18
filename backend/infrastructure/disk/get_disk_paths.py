import os

from config import CSV_DISK_DIR


def get_disk_paths(user_id: int) -> list[str]:
    user_dir = os.path.join(CSV_DISK_DIR, str(user_id))
    if not os.path.isdir(user_dir):
        return []
    return [
        os.path.join(user_dir, file_name)
        for file_name in os.listdir(user_dir)
        if os.path.isfile(os.path.join(user_dir, file_name))
    ]
