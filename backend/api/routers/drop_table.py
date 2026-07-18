from fastapi import APIRouter, Depends

from api.dependencies.require_login import require_login_api
from api.schemas.file_info import FileInfo
from api.services import drop_table_service

router = APIRouter()


@router.post("/drop-table", status_code=204)
def handle_drop_table(body: FileInfo, user_id: int = Depends(require_login_api)):
    drop_table_service.drop_table(user_id, body.file_name)
