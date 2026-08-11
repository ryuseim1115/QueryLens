from fastapi import APIRouter, Depends

from api.dependencies.require_login import require_login_api
from api.schemas.file_info import FileInfo
from api.services.csv_table import purge_file_service

router = APIRouter()


@router.delete("/purge-file", status_code=204)
def handle_purge_file(body: FileInfo, user_id: int = Depends(require_login_api)):
    purge_file_service.purge_file(user_id, body.file_name)
