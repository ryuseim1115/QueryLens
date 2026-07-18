import os

from infrastructure.disk.build_csv_path import build_csv_path


def save_csv(user_id: int, raw_file_name: str, file_content: bytes) -> None:

    try:
        file_content.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError(f"{raw_file_name} はCSV形式ではありません。")

    csv_path = build_csv_path(user_id, raw_file_name)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "wb") as f:
        f.write(file_content)
