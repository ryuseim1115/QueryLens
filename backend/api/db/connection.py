import duckdb
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_ID, REGION_NAME

connection = None


def get_connection() -> duckdb.DuckDBPyconnection:
    global connection
    if connection is None:
        connection = duckdb.connect()
        connection.execute("INSTALL httpfs; LOAD httpfs;")
        connection.execute(
            f""" SET s3_region='{REGION_NAME}';
            SET s3_access_key_id='{AWS_ACCESS_KEY_ID}';
            SET s3_secret_access_key='{AWS_SECRET_ACCESS_KEY_ID}';"""
        )
    return connection
