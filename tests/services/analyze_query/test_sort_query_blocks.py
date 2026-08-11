from api.schemas.run_query import QueryBlockAnalyzeResult
from api.services.analyze_query.query_block.sort_query_blocks import (
    sort_query_blocks_by_depth_desc,
)


def _make(depth: int) -> QueryBlockAnalyzeResult:
    return QueryBlockAnalyzeResult(
        start_index=0, end_index=10, query="SELECT 1", depth=depth, result=[]
    )


def test_sorts_descending():
    result = sort_query_blocks_by_depth_desc([_make(0), _make(2), _make(1)])
    assert [s.depth for s in result] == [2, 1, 0]


def test_single_element_unchanged():
    result = sort_query_blocks_by_depth_desc([_make(3)])
    assert result[0].depth == 3


def test_already_sorted_unchanged():
    result = sort_query_blocks_by_depth_desc([_make(2), _make(1), _make(0)])
    assert [s.depth for s in result] == [2, 1, 0]


def test_all_same_depth():
    result = sort_query_blocks_by_depth_desc([_make(1), _make(1), _make(1)])
    assert all(s.depth == 1 for s in result)
    assert len(result) == 3


def test_empty_input():
    result = sort_query_blocks_by_depth_desc([])
    assert result == []
