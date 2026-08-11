from fastapi import APIRouter, Depends

from api.dependencies.require_login import require_login_api
from api.schemas.file_info import FileInfo
from api.services.csv_table import create_table_service

router = APIRouter()


@router.post("/create-table", status_code=204)
def handle_create_table(body: FileInfo, user_id: int = Depends(require_login_api)):
    create_table_service.create_table(user_id, body.file_name)
