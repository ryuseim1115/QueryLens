from api.services.analyze_query.query_block.depth_analyzer import (
    get_query_block_depth,
)
from api.services.analyze_query.query_block.query_block import QueryBlock


# find_block_ranges_with_aliasで特定したブロックごとの範囲・エイリアスをもとに、
# 部分文字列の切り出し・ネスト深さの算出を行い、QueryBlockにまとめる
# （テーブル参照の抽出・解決はtable_reference.analyze_table_referencesが担う）
def build_query_blocks(
    query: str, block_ranges_alias: dict[tuple[int, int], str | None]
) -> list[QueryBlock]:
    query_blocks = []
    for (start, end), parent_alias in block_ranges_alias.items():
        # 範囲の包含関係から、このブロックのネスト深さを算出する
        depth = get_query_block_depth((start, end), block_ranges_alias.keys())

        # ブロックごとのクエリ文字列を切り出す例: (21, 38) -> "(SELECT * FROM b)"
        block_query = query[start:end]

        query_blocks.append(
            QueryBlock(
                start_index=start,
                end_index=end,
                query=block_query,
                depth=depth,
                parent_alias=parent_alias,
            )
        )

    return query_blocks
