from typing import Annotated

from fastapi import APIRouter, Depends, Form

from api.dependencies.require_login import require_login_api
from api.schemas.upload_csv import UploadCsvForm
from api.services.csv_table import upload_csv_service

router = APIRouter()


@router.post("/upload-csv", status_code=204)
def upload_csv(
    form: Annotated[UploadCsvForm, Form()],
    user_id: int = Depends(require_login_api),
):
    # アップロードされたファイルの中身を生のbytesとして読み込む
    file_content = form.file.file.read()
    upload_csv_service.save_csv(user_id, form.file.filename, file_content)
