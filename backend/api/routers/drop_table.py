from fastapi import APIRouter, Depends
from infrastructure.duckdb.drop_table import drop_table

from api.dependencies.require_login import require_login
from api.schemas.file_info import FileInfo

router = APIRouter()


@router.post(
    "/drop-csv-table", status_code=204, dependencies=[Depends(require_login)]
)
def handle_drop_table(body: FileInfo):
    drop_table(body.file_name)
