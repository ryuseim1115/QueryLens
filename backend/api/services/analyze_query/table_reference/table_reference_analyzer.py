from api.schemas.run_query import (
    QueryBlockAnalyzeResult,
    QueryBlockAnalyzeResultList,
    TableInfo,
)
from api.services.analyze_query.query_block.query_block import QueryBlock
from api.services.analyze_query.table_reference.table_block_matcher import (
    group_tables_by_block,
)
from api.services.analyze_query.table_reference.table_name_extractor import (
    extract_table_names_with_alias,
)
from api.services.analyze_query.table_reference.table_position_finder import (
    find_table_position,
)


# クエリ全体からテーブル参照を抽出してquery_blocksへ振り分けたうえで、
# それが実テーブルなのか他のQueryBlock（CTE/サブクエリ）を指しているのかを、
# query_blocks全体を見比べながら解決し、
# API応答用スキーマQueryBlockAnalyzeResultのリストに変換する
def analyze_table_references(
    query: str, query_blocks: list[QueryBlock]
) -> QueryBlockAnalyzeResultList:
    tables = extract_table_names_with_alias(query)
    tables_by_block = group_tables_by_block(
        tables,
        [
            (query_block.start_index, query_block.end_index)
            for query_block in query_blocks
        ],
    )

    return [
        QueryBlockAnalyzeResult(
            **vars(query_block),
            tables_name_alias=[
                _build_table_info(table_name, alias, position, query_blocks)
                for table_name, alias, position in tables_by_block[
                    (query_block.start_index, query_block.end_index)
                ]
            ],
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
