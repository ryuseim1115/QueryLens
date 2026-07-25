from api.services.query_structure.query_block_builder import QueryBlock


# tables_name_aliasの(table_name, alias)が実テーブルではなく、クエリ全体の中の
# 別のクエリブロック（CTEやサブクエリ）を指している場合、
# そのブロックの(start_index, end_index)を返す
#
# 実テーブルとCTE参照はsqlglotのAST上区別がつかない
# （どちらも"FROM t"はexp.Table(name="t")としてパースされる）ため、
# クエリ全体から得たquery_blocksのparent_alias
# （CTE名 or サブクエリのエイリアス）と突き合わせて判定する
# 例: "WITH t AS (SELECT * FROM a) SELECT * FROM t" の場合
#     ("t", None) はCTE "t" ブロックのparent_aliasと一致するため、
#     そのブロックの位置を返す
#     ("a", None) はどのブロックのparent_aliasとも一致しないため、
#     実テーブルとしてNoneを返す
def find_table_position(
    table_name: str | None, alias: str | None, query_blocks: list[QueryBlock]
) -> tuple[int, int] | None:
    identifier = table_name or alias
    if identifier is None:
        return None

    for query_block in query_blocks:
        if query_block.parent_alias == identifier:
            return query_block.start_index, query_block.end_index

    return None
