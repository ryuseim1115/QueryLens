from fastapi import APIRouter, Depends

from api.dependencies.require_login import require_login_api
from api.services.csv_table import file_table_status_service

router = APIRouter()


@router.get("/get-file-table-status")
def get_file_table_status(user_id: int = Depends(require_login_api)):
    return file_table_status_service.get_file_table_status(user_id)
