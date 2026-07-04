from config import S3_BUCKET_NAME

from infrastructure.duckdb.connection import get_connection


def create_table(file_name: str):
    path = f"s3://{S3_BUCKET_NAME}/{file_name}"
    table_name = file_name.removesuffix(".csv")
    connection = get_connection()
    sql = f"CREATE OR REPLACE TABLE \"{table_name}\" AS SELECT * FROM '{path}'"
    connection.sql(sql)
