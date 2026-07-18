import os

from dotenv import load_dotenv

load_dotenv()

TEMPLATES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)

MYSQL_URL = os.getenv("MYSQL_URL")

DATA_DIR = os.getenv("DATA_DIR", os.path.join(os.path.dirname(__file__), "data"))

# ファイル名は user_id から決まるため、ここではディレクトリのみ管理する
DUCKDB_DIR = os.getenv("DUCKDB_DIR", os.path.join(DATA_DIR, "duckdb"))

CSV_DISK_DIR = os.getenv("CSV_DISK_DIR", os.path.join(DATA_DIR, "csv_files"))

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
