from infrastructure.disk.get_disk_paths import get_disk_paths
from infrastructure.duckdb.get_table_names import get_table_names


def get_file_table_status(user_id: int) -> dict[str, list[str]]:
    # ディスク上の該当ユーザーの全ファイルのパス一覧を取得し、ファイル名だけのリストにする
    disk_paths = get_disk_paths(user_id)
    disk_files = [path.split("/")[-1] for path in disk_paths]

    # テーブル化済みの該当ユーザーのテーブル名を取得する
    table_names = get_table_names(user_id)

    tabled_files = [
        disk_file_name
        for disk_file_name in disk_files
        if disk_file_name.removesuffix(".csv") in table_names
    ]
    # テーブル化されていないファイルを「未テーブル化」とする
    untabled_files = [
        disk_file_name
        for disk_file_name in disk_files
        if disk_file_name not in tabled_files
    ]

    return {
        "tabled_files": tabled_files,
        "untabled_files": untabled_files,
    }
