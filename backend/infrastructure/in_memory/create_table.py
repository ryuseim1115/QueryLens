from config import S3_BUCKET_NAME

from infrastructure.in_memory.connection import get_connection, get_user_schema


def create_table(user_id: int, file_name: str):
    schema = get_user_schema(user_id)
    path = f"s3://{S3_BUCKET_NAME}/{user_id}/{file_name}"
    table_name = file_name.removesuffix(".csv")
    connection = get_connection()
    connection.sql(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
    sql = (
        f'CREATE OR REPLACE TABLE "{schema}"."{table_name}" '
        f"AS SELECT * FROM '{path}'"
    )
    connection.sql(sql)
