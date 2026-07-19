import os

from dotenv import load_dotenv

load_dotenv()

TEMPLATES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)

MYSQL_URL = os.getenv("MYSQL_URL")

DATA_DIR = os.getenv(
    "DATA_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
)

DUCKDB_DIR = os.getenv("DUCKDB_DIR", os.path.join(DATA_DIR, "duckdb"))

CSV_DISK_DIR = os.getenv("CSV_DISK_DIR", os.path.join(DATA_DIR, "csv_files"))

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

# セッションCookieの有効期限(秒)。
SESSION_MAX_AGE_SECONDS = 60 * 60
