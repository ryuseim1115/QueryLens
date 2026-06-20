import os

from dotenv import load_dotenv

load_dotenv()

CSV_FILES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "csv_files")
)

TEMPLATES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY_ID = os.getenv("AWS_SECRET_ACCESS_KEY_ID")
REGION_NAME = os.getenv("REGION_NAME")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
