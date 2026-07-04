import sqlglot
from sqlglot import errors, exp, parse_one

from infrastructure.duckdb.connection import get_connection


class QueryValidator:
    def __init__(self, database_type: str, query: str):
        self.database_type = database_type
        self.query = query

    def validate(self) -> sqlglot.Expression:
        try:
            expression = parse_one(self.query, read=self.database_type)
        except errors.ParseError as e:
            raise ValueError(f"SQL構文が正しくありません: {str(e)}")

        if expression.key != "select":
            raise ValueError("SELECT文以外の実行は許可されていません。")

        self._validate_tables(expression)
        return expression

    def _validate_tables(self, expression: sqlglot.Expression) -> None:
        cte_names = {cte.alias for cte in expression.find_all(exp.CTE)}
        query_tables = {
            table.name
            for table in expression.find_all(exp.Table)
            if table.name and table.name not in cte_names
        }
        if not query_tables:
            return

        connection = get_connection()
        existing = {row[0] for row in connection.sql("SHOW TABLES").fetchall()}
        missing = query_tables - existing
        if missing:
            raise ValueError(
                "次のテーブルに対応するCSVファイルがアップロードされていません: "
                f"{', '.join(sorted(missing))}"
            )
