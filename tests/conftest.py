import os

import pytest

from api.db.create_csv_tables import create_csv_tables

CSV_FILES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "csv_files")
)


@pytest.fixture(scope="session", autouse=True)
def setup_csv_tables():
    csv_files = sorted(f for f in os.listdir(CSV_FILES_DIR) if f.endswith(".csv"))
    create_csv_tables(CSV_FILES_DIR, csv_files)
