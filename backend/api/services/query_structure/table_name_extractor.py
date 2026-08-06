from api.services.query_structure.query_parser import parse_query_block
from sqlglot import exp

TableNameAlias = tuple[str | None, str | None, tuple[int, int] | None]


def extract_table_names_with_alias(
    block_query: str, start: int
) -> list[TableNameAlias]:
    # block_queryをパースしたAST上で、直下のFROM/JOIN、SELECT句のスカラーサブクエリ
    # だけを見る。（サブクエリの中身までは再帰しない）
    # 例: "SELECT (SELECT * FROM C) D FROM A JOIN (SELECT * FROM E) B"
    #   -> [("A", None, (33, 34)), (None, "B", (56, 57)), (None, "D", (24, 25))]
    #      A: 実テーブルなのでテーブル名のみ（エイリアスなし）
    #      B: JOIN対象サブクエリ全体に付いたエイリアス。テーブル名はないためNone
    #      D: SELECT句の列として直接エイリアスされたスカラーサブクエリ。同様にNone
    #      C, E: サブクエリの中身（別のクエリブロック）なので、ここでは抽出されない
    #      各タプル末尾は、そのテーブル/エイリアスが元クエリ文字列上で
    #      実際に書かれている位置（(start, end)、テーブル名のみを着色する用途）
    expression, offset = parse_query_block(block_query)
    base_offset = start + offset

    tables = []
    from_expression = expression.args.get("from_")
    if from_expression:
        table_name_alias = _get_table_name_and_alias(from_expression.this, base_offset)
        if any(table_name_alias[:2]):
            tables.append(table_name_alias)

    for join in expression.args.get("joins") or []:
        table_name_alias = _get_table_name_and_alias(join.this, base_offset)
        if any(table_name_alias[:2]):
            tables.append(table_name_alias)

    # SELECT句の列として直接エイリアスされたスカラーサブクエリも対象にする
    # 例: "SELECT (SELECT COUNT(*) FROM orders) AS order_count FROM users"
    #   -> ("order_count"というエイリアスのみ、実テーブルではないためNone)
    #      式の一部に埋もれたサブクエリ（例: "(SELECT ...) + 1 AS total"）は対象外
    for select_expression in expression.args.get("expressions") or []:
        if isinstance(select_expression, exp.Alias) and isinstance(
            select_expression.this, exp.Subquery
        ):
            alias_node = select_expression.args.get("alias")
            tables.append(
                (None, select_expression.alias, _get_position(alias_node, base_offset))
            )

    return tables


def _get_table_name_and_alias(node, base_offset: int) -> TableNameAlias:
    # 実テーブルの場合はテーブル名とエイリアス（あれば）の両方を取得
    # 位置は実際にクエリ上に書かれているテーブル名の識別子（エイリアスではない）を使う
    if isinstance(node, exp.Table):
        position = _get_position(node.this, base_offset)
        return node.name or None, node.alias or None, position
    if isinstance(node, exp.Subquery):
        # サブクエリにはテーブル名が存在しないためNone、エイリアスのみ取得
        # 位置も、クエリ上に書かれているのはエイリアスのみのためエイリアスの識別子を使う
        alias_node = node.args.get("alias")
        identifier = alias_node.this if alias_node else None
        return None, node.alias or None, _get_position(identifier, base_offset)
    # VALUES句やUNNESTなど、実テーブル/サブクエリ以外の場合は(None, None, None)
    return None, None, None


def _get_position(identifier, base_offset: int) -> tuple[int, int] | None:
    if identifier is None:
        return None
    meta = identifier.meta
    if "start" not in meta or "end" not in meta:
        return None
    return base_offset + meta["start"], base_offset + meta["end"] + 1
