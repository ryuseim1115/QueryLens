from infrastructure.security.strip_path import strip_path
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel

from api.validators.csv_file_name_validator import CsvFileNameValidator


# UploadCsvFormからも直接呼べるよう、クラスに依存しない関数として切り出している
def validate_csv_file_name(value: str) -> str:
    # この後ファイルパスの組み立てに使われるため、境界であるスキーマの時点で
    # パストラバーサル対策を済ませておく
    value = strip_path(value)

    # file_nameはテーブル名の組み立て(DROP TABLE等のSQL文字列)にも使われるため、
    # 識別子として安全な文字だけを許可する
    CsvFileNameValidator(value).validate()
    return value


class FileInfo(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )
    file_name: str

    @field_validator("file_name")
    # _validate_file_name()はインスタンス化(パース)の途中で呼ばれ、
    # まだインスタンスが未完成のため、selfではなくclsを受け取る
    @classmethod
    def _validate_file_name(cls, value: str) -> str:
        return validate_csv_file_name(value)
