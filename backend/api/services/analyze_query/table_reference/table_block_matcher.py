from collections.abc import Iterable

from api.services.analyze_query.table_reference.table_name_extractor import (
    TableNameAlias,
)


# extract_table_names_with_aliasで抽出した(テーブル名, エイリアス, 位置)のリストを、
# それぞれの位置を包含する最小のブロック範囲（＝直接参照している側のブロック）
# ごとに振り分ける
def group_tables_by_block(
    tables: list[TableNameAlias],
    block_ranges: Iterable[tuple[int, int]],
) -> dict[tuple[int, int], list[TableNameAlias]]:
    ranges = list(block_ranges)
    grouped: dict[tuple[int, int], list[TableNameAlias]] = {
        block_range: [] for block_range in ranges
    }

    for table in tables:
        owning_block = _find_owning_block(table[2], ranges)
        grouped[owning_block].append(table)

    return grouped


# positionを完全に包含するブロック範囲のうち、最も範囲が狭いもの
# （＝直下の親ブロック。サブクエリ等のより深いブロックほど範囲が狭くなる）を返す
# rangesには常にクエリ全体のブロックが含まれるため、通常は必ず1つ以上見つかるはず
def _find_owning_block(
    position: tuple[int, int],
    ranges: list[tuple[int, int]],
) -> tuple[int, int]:
    position_start, position_end = position
    containing_blocks = [
        block_range
        for block_range in ranges
        if block_range[0] <= position_start and position_end <= block_range[1]
    ]
    if not containing_blocks:
        raise ValueError(f"positionを含むブロックが見つかりません: {position}")

    # ブロック範囲の幅（広いほど外側、狭いほど内側のブロック）
    def block_width(block_range: tuple[int, int]) -> int:
        return block_range[1] - block_range[0]

    # 幅が最小＝最も内側（直下）のブロックを選ぶ
    return min(containing_blocks, key=block_width)
