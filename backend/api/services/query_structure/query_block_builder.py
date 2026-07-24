from dataclasses import dataclass

import sqlglot
from api.services.query_structure.depth_analyzer import get_query_block_depths
from api.services.query_structure.query_parser import parse_query_block
from api.services.query_structure.range_finder import (
    find_cte_ranges,
    find_subquery_ranges,
)
from api.services.query_structure.table_name_extractor import (
    extract_table_names_with_alias,
)


@dataclass
class QueryBlock:
    start_index: int
    end_index: int
    query: str
    depth: int
    tables_name_alias: list[tuple[str | None, str | None]]
    parent_alias: str | None = None


# クエリ文字列をトークン化し、サブクエリ/CTEの範囲・ネスト深さ・参照テーブルを解析して
# 内部表現QueryBlockのリストを組み立てる
# （API応答用スキーマへの変換はanalyze_query_structureが担う）
def build_query_blocks(query: str) -> list[QueryBlock]:
    # クエリ全体をトークン列に分解する（範囲特定はASTではなくトークン単位で行うため）
    tokens = sqlglot.tokens.Tokenizer().tokenize(query)

    # 括弧で囲まれたサブクエリ（クエリ全体も含む）の(start, end)範囲とエイリアスを特定
    # 例: "SELECT * FROM a JOIN (SELECT * FROM b) c"
    # -> {(0, 40): None, (21, 38): "c"}
    #    (0, 40) はクエリ全体自身の範囲（エイリアスは存在しないためNone）
    #    (21, 38) は "(SELECT * FROM b)" の範囲、エイリアスは "c"
    subquery_ranges_alias = find_subquery_ranges(query, tokens)

    # WITH句で定義されたCTEの(start, end)範囲とCTE名を特定
    # 例: "WITH t AS (SELECT * FROM a) SELECT * FROM t"
    # -> {(10, 27): "t"}
    #    (10, 27) は "(SELECT * FROM a)" の範囲、CTE名は "t"
    cte_ranges_alias = find_cte_ranges(tokens)

    # ブロック（クエリ全体・CTE・サブクエリ）ごとの範囲一覧
    # 例（"SELECT * FROM a JOIN (SELECT * FROM b) c" の場合）: [(0, 40), (21, 38)]
    ranges = list(subquery_ranges_alias.keys())

    # 各範囲について、自身を包含する範囲の数からネストの深さを算出
    # 例: [(0, 40), (21, 38)] -> [0, 1]
    #    (0, 40)はクエリ全体なので深さ0、(21, 38)はその内側なので深さ1
    depths = get_query_block_depths(ranges)

    # 各範囲に対応する部分文字列を切り出す（ブロックごとのクエリ文字列）
    # 例: [(0, 40), (21, 38)]
    # -> ["SELECT * FROM a JOIN (SELECT * FROM b) c", "(SELECT * FROM b)"]
    block_queries = [query[start:end] for start, end in ranges]

    # expressions は、block_queries を sqlglot でパースした AST
    # (exp.Expression)のリスト
    # 例: "SELECT id FROM users"
    # -> Select(expressions=[Column(...)], from_=From(this=Table(...)))
    expressions = [parse_query_block(block_query) for block_query in block_queries]

    # 各ブロックのASTから、直下のFROM/JOINが参照するテーブル名・エイリアスを抽出
    # 例: ["SELECT * FROM a JOIN (SELECT * FROM b) c", "(SELECT * FROM b)"]
    # -> [[("a", None), (None, "c")], [("b", None)]]
    #    1つ目のブロックでは実テーブル"a"（エイリアスなし）と、
    #    "c"というエイリアスの付いたサブクエリ
    #    （実テーブルではないため名前はNone）を参照している
    query_block_tables_name_alias = [
        extract_table_names_with_alias(expression) for expression in expressions
    ]

    # ここまでで求めた範囲・深さ・参照テーブルをブロック単位でQueryBlockにまとめる
    query_blocks = []
    for (start, end), block_query, depth, tables_name_alias in zip(
        ranges, block_queries, depths, query_block_tables_name_alias
    ):
        query_blocks.append(
            QueryBlock(
                start_index=start,
                end_index=end,
                query=block_query,
                depth=depth,
                tables_name_alias=tables_name_alias,
                # CTEとサブクエリは同じ範囲になり得ないため、
                # どちらか一方だけが取得できる
                parent_alias=cte_ranges_alias.get((start, end))
                or subquery_ranges_alias.get((start, end)),
            )
        )

    return query_blocks
