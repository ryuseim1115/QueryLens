from sqlglot import exp


def extract_table_names_with_alias(
    expression: exp.Expression,
) -> list[tuple[str | None, str | None]]:
    # このexpression直下のFROM/JOINだけを見る。サブクエリの中身までは再帰しない
    # 例: "SELECT * FROM A JOIN (SELECT * FROM C) B"
    #   -> [("A", None), (None, "B")]
    #      A: 実テーブルなのでテーブル名のみ（エイリアスなし）
    #      B: サブクエリ全体に付いたエイリアス。サブクエリ自体にテーブル名はないためNone
    #      C: サブクエリの中身（別のクエリブロック）なので、ここでは抽出されない
    tables = []
    from_expression = expression.args.get("from_")
    if from_expression:
        table_name_alias = _get_table_name_and_alias(from_expression.this)
        if any(table_name_alias):
            tables.append(table_name_alias)

    for join in expression.args.get("joins") or []:
        table_name_alias = _get_table_name_and_alias(join.this)
        if any(table_name_alias):
            tables.append(table_name_alias)
    return tables


def _get_table_name_and_alias(node) -> tuple[str | None, str | None]:
    # 実テーブルの場合はテーブル名とエイリアス（あれば）の両方を取得
    if isinstance(node, exp.Table):
        return node.name or None, node.alias or None
    if isinstance(node, exp.Subquery):
        # サブクエリにはテーブル名が存在しないためNone、エイリアスのみ取得
        return None, node.alias or None
    # VALUES句やUNNESTなど、実テーブル/サブクエリ以外の場合は(None, None)
    return None, None
