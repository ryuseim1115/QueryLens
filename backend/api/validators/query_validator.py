import sqlglot
from infrastructure.duckdb.get_table_names import get_table_names
from sqlglot import errors, exp, parse_one


# database_typeとqueryの2つだけで完結する純粋な構文チェックのため、
# サービス層からだけでなくQueryInfo/RunQueryBlockRequestのmodel_validatorからも
# 直接呼べるよう、クラスに依存しない関数として切り出している。
# こうすることで「SELECT文以外禁止」がスキーマの境界で型ヒント駆動に強制され、
# サービス層で呼び出しを書き忘れても素通りしない。
def parse_select_query(database_type: str, query: str) -> sqlglot.Expression:
    query = query.strip()
    # ブロック単体のクエリ文字列は外側に括弧が付いたまま渡されることがあり
    # （例: "(SELECT ...)"）、そのままだとsqlglotが"subquery"型と解釈してしまい
    # SELECT文判定に失敗するため剥がす
    if query.startswith("(") and query.endswith(")"):
        query = query[1:-1].strip()

    try:
        expression = parse_one(query, read=database_type)
    except errors.ParseError as e:
        raise ValueError(f"SQL構文が正しくありません: {str(e)}")

    if expression.key != "select":
        raise ValueError("SELECT文以外の実行は許可されていません。")

    return expression


class QueryValidator:
    def __init__(self, database_type: str, query: str, user_id: int):
        self.database_type = database_type
        self.query = query
        self.user_id = user_id

    def validate(self) -> sqlglot.Expression:
        expression = parse_select_query(self.database_type, self.query)
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
