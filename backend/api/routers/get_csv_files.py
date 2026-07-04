from fastapi import APIRouter
from infrastructure.s3.get_csv_paths import get_csv_paths

router = APIRouter()


@router.get("/get-csv-files")
def get_csv_files():
    csv_paths = get_csv_paths()
    csv_files = [path.split("/")[-1] for path in csv_paths]
    return {"csv_files": csv_files}
