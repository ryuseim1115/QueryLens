import os

from api.validators.csv_file_name_validator import CsvFileNameValidator
from config import CSV_DISK_DIR

from infrastructure.security.strip_path import strip_path


# CSVファイルの実パスはこの関数を通してのみ組み立てる。
# strip_path/CsvFileNameValidatorの呼び出しをここに集約することで、
# 個々の呼び出し元での書き忘れ(パストラバーサル)を構造的に防ぐ
def build_csv_path(user_id: int, raw_file_name: str) -> str:
    file_name = strip_path(raw_file_name)
    CsvFileNameValidator(file_name).validate()
    return os.path.join(CSV_DISK_DIR, str(user_id), file_name)
