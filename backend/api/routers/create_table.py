import duckdb
from fastapi import APIRouter, Depends, HTTPException
from infrastructure.in_memory.create_table import create_table

from api.dependencies.require_login import require_login_api
from api.schemas.file_info import FileInfo

router = APIRouter()


@router.post("/create-table", status_code=204)
def handle_create_table(body: FileInfo, user_id: int = Depends(require_login_api)):
    try:
        create_table(user_id, body.file_name)
    except duckdb.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
