from api.db.connection import get_connection
from api.schemas.run_query import SubqueryAnalyzeResultList


def run_subqueries(subqueries: SubqueryAnalyzeResultList) -> SubqueryAnalyzeResultList:
    connection = get_connection()
    for subquery in subqueries:
        try:
            result = connection.sql(subquery.query)
            subquery.result = [
                dict(zip(result.columns, record)) for record in result.fetchall()
            ]
        except Exception as e:
            raise ValueError(f"サブクエリの実行に失敗しました: {e}")
    return subqueries
