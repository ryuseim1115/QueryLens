from fastapi import APIRouter, Depends
from infrastructure.in_memory.get_in_memory_table_names import get_in_memory_table_names
from infrastructure.storage.get_storage_paths import get_storage_paths

from api.dependencies.require_login import require_login_api

router = APIRouter()


@router.get("/get-file-memory-status")
def get_file_memory_status(user_id: int = Depends(require_login_api)):
    # S3上の該当ユーザーの全ファイルのパス一覧を取得し、ファイル名だけのリストにする
    storage_paths = get_storage_paths(user_id)
    storage_files = [path.split("/")[-1] for path in storage_paths]

    # インメモリに存在する該当ユーザーのテーブル名を取得する
    memory_table_names = get_in_memory_table_names(user_id)

    in_memory_files = [
        storage_file_name
        for storage_file_name in storage_files
        if storage_file_name.removesuffix(".csv") in memory_table_names
    ]
    # インメモリでないファイルを「未インメモリ」とする
    not_in_memory_files = [
        storage_file_name
        for storage_file_name in storage_files
        if storage_file_name not in in_memory_files
    ]

    return {
        "in_memory_files": in_memory_files,
        "not_in_memory_files": not_in_memory_files,
    }
