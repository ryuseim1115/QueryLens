import sqlglot
from infrastructure.duckdb.get_table_names import get_table_names
from sqlglot import errors, exp, parse_one


class QueryValidator:
    def __init__(self, database_type: str, query: str, user_id: int):
        self.database_type = database_type
        self.query = query
        self.user_id = user_id

    def validate(self) -> sqlglot.Expression:
        query = self.query.strip()
        # ブロック単体のクエリ文字列は外側に括弧が付いたまま渡されることがあり
        # （例: "(SELECT ...)"）、そのままだとsqlglotが"subquery"型と解釈してしまい
        # SELECT文判定に失敗するため剥がす
        if query.startswith("(") and query.endswith(")"):
            query = query[1:-1].strip()

        try:
            expression = parse_one(query, read=self.database_type)
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

        table_names = get_table_names(self.user_id)
        missing = query_tables - table_names
        if missing:
            raise ValueError(
                "次のテーブルに対応するファイルがアップロードされていません: "
                f"{', '.join(sorted(missing))}"
            )
