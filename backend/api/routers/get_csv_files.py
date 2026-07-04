from fastapi import APIRouter, Depends
from infrastructure.s3.get_csv_paths import get_csv_paths

from api.dependencies.require_login import require_login

router = APIRouter()


@router.get("/get-csv-files", dependencies=[Depends(require_login)])
def get_csv_files():
    csv_paths = get_csv_paths()
    csv_files = [path.split("/")[-1] for path in csv_paths]
    return {"csv_files": csv_files}
