from infrastructure.security.strip_path import strip_path
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel

from api.validators.csv_file_name_validator import CsvFileNameValidator


class FileInfo(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )
    file_name: str

    # ここで受け取ったfile_nameはこの後ファイルパスの組み立てに使われるため、
    # 境界であるスキーマの時点でパストラバーサル対策を済ませておく

    # インスタンス化されるたびに_strip_path()が実行されるようにする
    @field_validator("file_name")
    # _strip_path()はインスタンス化(パース)の途中で呼ばれ、
    # まだインスタンスが未完成のため、selfではなくclsを受け取る
    @classmethod
    def _strip_path(cls, value: str) -> str:
        return strip_path(value)

    # file_nameはテーブル名の組み立て(DROP TABLE等のSQL文字列)にも使われるため、
    # 識別子として安全な文字だけを許可する
    @field_validator("file_name")
    @classmethod
    def _validate_chars(cls, value: str) -> str:
        CsvFileNameValidator(value).validate()
        return value
