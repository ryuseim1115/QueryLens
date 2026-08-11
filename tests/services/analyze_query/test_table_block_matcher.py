import pytest
from api.services.analyze_query.table_reference.table_block_matcher import (
    group_tables_by_block,
)


def test_table_in_only_block_is_grouped_to_it():
    # (10, 20)の中に位置する参照は、そのブロックに振り分けられる
    tables = [("users", None, (12, 17))]
    result = group_tables_by_block(tables, [(0, 30), (10, 20)])
    assert result[(10, 20)] == [("users", None, (12, 17))]
    assert result[(0, 30)] == []


def test_table_is_grouped_to_innermost_enclosing_block():
    # 複数のブロックに包含される場合、最も範囲の狭い(=直下の)ブロックに振り分ける
    table = ("users", None, (14, 19))
    tables = [table]
    result = group_tables_by_block(tables, [(0, 30), (5, 25), (10, 20)])
    assert result[(10, 20)] == [table]
    assert result[(0, 30)] == []
    assert result[(5, 25)] == []


def test_all_block_ranges_are_present_even_when_empty():
    result = group_tables_by_block([], [(0, 30), (10, 20)])
    assert result == {(0, 30): [], (10, 20): []}


def test_table_outside_any_block_raises():
    tables = [("users", None, (100, 105))]
    with pytest.raises(ValueError, match="positionを含むブロックが見つかりません"):
        group_tables_by_block(tables, [(0, 30)])
