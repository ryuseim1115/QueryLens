from fastapi import APIRouter

from api.db.create_table import create_table
from api.schemas.file_info import FileInfo

router = APIRouter()


@router.post("/create-csv-table", status_code=204)
def handle_create_table(body: FileInfo):
    create_table(body.file_name)
