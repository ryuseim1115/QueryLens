from fastapi import APIRouter

from infrastructure.duckdb.drop_table import drop_table
from api.schemas.file_info import FileInfo

router = APIRouter()


@router.post("/drop-csv-table", status_code=204)
def handle_drop_table(body: FileInfo):
    drop_table(body.file_name)
