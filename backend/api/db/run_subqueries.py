import os

import duckdb
from config import CSV_FILES_DIR

from api.schemas.run_query import SubqueryAnalyzeResultList


def run_subqueries(subqueries: SubqueryAnalyzeResultList) -> SubqueryAnalyzeResultList:
    connection = duckdb.connect()
    for csv_file in os.listdir(CSV_FILES_DIR):
        if csv_file.endswith(".csv"):
            table_name = csv_file.removesuffix(".csv")
            csv_path = os.path.join(CSV_FILES_DIR, csv_file)
            connection.execute(
                f'CREATE TABLE "{table_name}" AS '
                f'SELECT * FROM read_csv_auto("{csv_path}")'
            )
    for subquery in subqueries:
        try:
            result = connection.sql(subquery.query)
            subquery.result = [
                dict(zip(result.columns, record)) for record in result.fetchall()
            ]
        except Exception as e:
            raise ValueError(f"サブクエリの実行に失敗しました: {e}")
    return subqueries
