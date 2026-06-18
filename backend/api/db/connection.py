import duckdb
from config import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY_ID,REGION_NAME

def get_connection() -> duckdb.DuckDBPyconnection:
    connection = duckdb.connect()
    connection.execute("INSTALL httpfs; LOAD httpfs;")
    connection.execute(f""" SET s3_region='{REGION_NAME}';
      SET s3_access_key_id='{AWS_ACCESS_KEY_ID}';
      SET s3_secret_access_key='{AWS_SECRET_ACCESS_KEY_ID}';""")
    return connection
