from api.schemas.run_query import (
    QueryBlockAnalyzeResult,
    QueryBlockAnalyzeResultList,
    TableInfo,
)
from api.services.query_structure.block_range_alias_finder import (
    find_block_ranges_with_alias,
)
from api.services.query_structure.depth_analyzer import get_query_block_depth
from api.services.query_structure.table_name_extractor import (
    extract_table_names_with_alias,
)
from api.services.query_structure.table_position_finder import find_table_position
from api.services.query_structure.types.query_block import QueryBlock


# サブクエリ/CTEの範囲・ネスト深さ・参照テーブルを解析する
def analyze_query_structure(query: str) -> list[QueryBlock]:
    # クエリをブロックに分解し、それぞれの範囲・エイリアスを特定
    block_ranges_alias = find_block_ranges_with_alias(query)
    ranges = list(block_ranges_alias.keys())

    # 各ブロックについて、部分文字列の切り出し・ASTパース・参照テーブル抽出を行い、QueryBlockにまとめる
    query_blocks = []
    for (start, end), parent_alias in block_ranges_alias.items():
        # 範囲の包含関係から、このブロックのネスト深さを算出する
        depth = get_query_block_depth((start, end), ranges)

        # ブロックごとのクエリ文字列を切り出す例: (21, 38) -> "(SELECT * FROM b)"
        block_query = query[start:end]

        # block_queryをASTパースし、直下のFROM/JOINが参照するテーブル名・エイリアスと、それらが元クエリ文字列上で実際に書かれている位置を抽出する
        # 例: "SELECT * FROM a JOIN (SELECT * FROM b) c"　-> [("a", None, (14, 15)), (None, "c", (39, 40))]
        tables_name_alias = extract_table_names_with_alias(block_query, start)

        query_blocks.append(
            QueryBlock(
                start_index=start,
                end_index=end,
                query=block_query,
                depth=depth,
                tables_name_alias=tables_name_alias,
                parent_alias=parent_alias,
            )
        )

    return query_blocks


# 各QueryBlockのテーブル参照が実テーブルなのか他のQueryBlock（CTE/サブクエリ）を
# 指しているのかを、query_blocks全体を見比べながら解決し、
# API応答用スキーマQueryBlockAnalyzeResultのリストに変換する
def resolve_table_references(
    query_blocks: list[QueryBlock],
) -> QueryBlockAnalyzeResultList:
    return [
        QueryBlockAnalyzeResult(
            start_index=query_block.start_index,
            end_index=query_block.end_index,
            query=query_block.query,
            depth=query_block.depth,
            tables_name_alias=[
                _build_table_info(table_name, alias, position, query_blocks)
                for table_name, alias, position in query_block.tables_name_alias
            ],
            parent_alias=query_block.parent_alias,
            result=[],
        )
        for query_block in query_blocks
    ]


def _build_table_info(
    table_name: str | None,
    alias: str | None,
    position: tuple[int, int] | None,
    query_blocks: list[QueryBlock],
) -> TableInfo:
    referenced_block_position = find_table_position(table_name, alias, query_blocks)
    return TableInfo(
        table_name=table_name,
        alias=alias,
        start_index=position[0] if position else None,
        end_index=position[1] if position else None,
        referenced_block_start_index=(
            referenced_block_position[0] if referenced_block_position else None
        ),
        referenced_block_end_index=(
            referenced_block_position[1] if referenced_block_position else None
        ),
    )
