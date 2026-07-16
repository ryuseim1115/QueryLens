from fastapi import APIRouter, Depends
from infrastructure.in_memory.drop_table import drop_table
from infrastructure.storage.delete_storage_file import delete_storage_file

from api.dependencies.require_login import require_login_api
from api.schemas.file_info import FileInfo

router = APIRouter()


@router.delete("/purge-file", status_code=204)
def handle_purge_file(body: FileInfo, user_id: int = Depends(require_login_api)):
    drop_table(user_id, body.file_name)
    delete_storage_file(user_id, body.file_name)
