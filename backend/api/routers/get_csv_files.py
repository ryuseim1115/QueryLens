from fastapi import APIRouter, Depends
from infrastructure.duckdb.connection import get_connection
from infrastructure.s3.get_csv_paths import get_csv_paths

from api.dependencies.require_login import require_login

router = APIRouter()


@router.get("/get-csv-files", dependencies=[Depends(require_login)])
def get_csv_files():
    csv_paths = get_csv_paths()
    csv_files = [path.split("/")[-1] for path in csv_paths]

    connection = get_connection()
    existing_tables = {row[0] for row in connection.sql("SHOW TABLES").fetchall()}
    untabled_files = [
        file_name
        for file_name in csv_files
        if file_name.removesuffix(".csv") not in existing_tables
    ]

    return {"csv_files": csv_files, "untabled_files": untabled_files}
