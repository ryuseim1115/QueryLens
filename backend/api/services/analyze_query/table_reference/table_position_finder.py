from api.services.analyze_query.query_block.query_block import QueryBlock


# table_name/aliasが実テーブルではなく別のクエリブロック（CTE/サブクエリ）を
# 指している場合、そのブロックの(start_index, end_index)を返す
# 例: "WITH t AS (...) SELECT * FROM t" の "t" -> CTEブロックの位置
#     "SELECT * FROM a" の "a" -> どこにも一致しないので実テーブル(None)
def find_table_position(
    table_name: str | None, alias: str | None, query_blocks: list[QueryBlock]
) -> tuple[int, int] | None:
    identifier = table_name or alias
    if identifier is None:
        raise ValueError("table_nameとaliasが両方Noneの参照が渡されました")

    for query_block in query_blocks:
        if query_block.parent_alias == identifier:
            # CTE/サブクエリのブロックの位置を返す
            return query_block.start_index, query_block.end_index
    # 実テーブルである時
    return None
