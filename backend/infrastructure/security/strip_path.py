import os


# ファイル名にディレクトリ区切りが含まれると、CSV_DISK_DIR配下を組み立てる際に
# 意図した保存先の外を指してしまう（パストラバーサル）ため、
# ファイル名部分だけに切り詰める
# 例:
#   "reviews.csv"         -> "reviews.csv"
#   "../../etc/passwd"    -> "passwd"
#   "foo/bar/reviews.csv" -> "reviews.csv"
def strip_path(file_name: str) -> str:
    return os.path.basename(file_name)
