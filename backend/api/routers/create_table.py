from fastapi import APIRouter, Depends
from infrastructure.duckdb.create_table import create_table

from api.dependencies.require_login import require_login
from api.schemas.file_info import FileInfo

router = APIRouter()


@router.post(
    "/create-csv-table", status_code=204, dependencies=[Depends(require_login)]
)
def handle_create_table(body: FileInfo):
    create_table(body.file_name)
