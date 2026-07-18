from fastapi import APIRouter, Depends, File, UploadFile

from api.dependencies.require_login import require_login_api
from api.services import upload_csv_service

router = APIRouter()


@router.post("/upload-csv", status_code=204)
def upload_csv(file: UploadFile = File(...), user_id: int = Depends(require_login_api)):
    # アップロードされたファイルの中身を生のbytesとして読み込む
    file_content = file.file.read()
    upload_csv_service.save_csv(user_id, file.filename, file_content)
