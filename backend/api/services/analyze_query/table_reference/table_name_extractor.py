import sqlglot
from sqlglot import exp

TableNameAlias = tuple[str | None, str | None, tuple[int, int] | None]


# ネストの深さに関わらず全SELECTのFROM/JOIN参照先のテーブルと、
# それらが元クエリ文字列上で実際に書かれている位置を抽出する
# （どのブロックに属するかは呼び出し側がpositionをもとに判定する）
# 例: "SELECT * FROM a JOIN (SELECT * FROM b) c"
# -> [("a", None, (14, 15)), (None, "c", (39, 40))]
def extract_table_names_with_alias(query: str) -> list[TableNameAlias]:
    expression = sqlglot.parse_one(query)

    return [
        table
        for select_expression in expression.find_all(exp.Select)
        for table in (
            *_extract_from_join_tables(select_expression),
            *_extract_scalar_subquery_aliases(select_expression),
        )
    ]


# FROM句・JOIN句が指すテーブル/サブクエリを抽出する
def _extract_from_join_tables(expression: exp.Expression) -> list[TableNameAlias]:
    from_expression = expression.args.get("from_")
    from_tables = [from_expression.this] if from_expression else []
    join_tables = [join.this for join in expression.args.get("joins") or []]

    tables = (_get_table_name_and_alias(node) for node in from_tables + join_tables)
    # テーブル名・エイリアスがどちらも取れない場合（VALUES句等）は対象外
    return [table for table in tables if any(table[:2])]


# SELECT句の列として直接エイリアスされたスカラーサブクエリを抽出する
# 例: "SELECT (SELECT COUNT(*) FROM orders) AS order_count FROM users"
#   -> ("order_count"というエイリアスのみ、実テーブルではないためNone)
#      式の一部に埋もれたサブクエリ（例: "(SELECT ...) + 1 AS total"）は対象外
def _extract_scalar_subquery_aliases(
    expression: exp.Expression,
) -> list[TableNameAlias]:
    return [
        (None, column.alias, _get_position(column.args.get("alias")))
        for column in expression.args.get("expressions") or []
        if _is_scalar_subquery_alias(column)
    ]


# SELECT句の列が「サブクエリ本体に直接エイリアスがついている」形かどうかを判定する
# 例: "(SELECT COUNT(*) FROM orders) AS order_count" -> True
#     式の一部に埋もれている場合（例: "(SELECT ...) + 1 AS total"）はFalse
def _is_scalar_subquery_alias(column_expression: exp.Expression) -> bool:
    return isinstance(column_expression, exp.Alias) and isinstance(
        column_expression.this, exp.Subquery
    )


# 実テーブル/サブクエリのノードからテーブル名・エイリアス・位置を取得する
def _get_table_name_and_alias(node: exp.Expression) -> TableNameAlias:
    # 実テーブルの場合はテーブル名とエイリアス（あれば）の両方を取得
    # 位置は実際にクエリ上に書かれているテーブル名の識別子（エイリアスではない）を使う
    if isinstance(node, exp.Table):
        position = _get_position(node.this)
        return node.name or None, node.alias or None, position
    if isinstance(node, exp.Subquery):
        # サブクエリにはテーブル名が存在しないためNone、エイリアスのみ取得
        # 位置も、クエリ上に書かれているのはエイリアスのみのためエイリアスの識別子を使う
        alias_node = node.args.get("alias")
        identifier = alias_node.this if alias_node else None
        return None, node.alias or None, _get_position(identifier)
    # VALUES句やUNNESTなど、実テーブル/サブクエリ以外の場合は(None, None, None)
    return None, None, None


def _get_position(identifier) -> tuple[int, int] | None:
    if identifier is None:
        return None
    meta = identifier.meta
    if "start" not in meta or "end" not in meta:
        return None
    return meta["start"], meta["end"] + 1
