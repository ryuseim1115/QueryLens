from fastapi import UploadFile
from pydantic import BaseModel, field_validator

from api.schemas.file_info import validate_csv_file_name


class UploadCsvForm(BaseModel):
    file: UploadFile

    # FileInfoのfile_nameと同じ規則をアップロード時のファイル名にも適用する
    @field_validator("file")
    @classmethod
    def _validate_file_name(cls, value: UploadFile) -> UploadFile:
        value.filename = validate_csv_file_name(value.filename or "")
        return value
