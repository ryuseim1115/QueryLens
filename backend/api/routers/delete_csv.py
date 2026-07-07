from fastapi import APIRouter, Depends
from infrastructure.duckdb.drop_table import drop_table
from infrastructure.s3.delete_csv import delete_csv

from api.dependencies.require_login import require_login
from api.schemas.file_info import FileInfo

router = APIRouter()


@router.delete(
    "/delete-csv-file", status_code=204, dependencies=[Depends(require_login)]
)
def handle_delete_csv(body: FileInfo):
    drop_table(body.file_name)
    delete_csv(body.file_name)
