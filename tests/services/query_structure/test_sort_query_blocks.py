from api.schemas.run_query import QueryBlockAnalyzeResult
from api.services.query_structure.sort_query_blocks import SortQueryBlocksByDepthDesc


def _make(depth: int) -> QueryBlockAnalyzeResult:
    return QueryBlockAnalyzeResult(
        start_index=0, end_index=10, query="SELECT 1", depth=depth, result=[]
    )


def test_sorts_descending():
    result = SortQueryBlocksByDepthDesc([_make(0), _make(2), _make(1)]).execute()
    assert [s.depth for s in result] == [2, 1, 0]


def test_single_element_unchanged():
    result = SortQueryBlocksByDepthDesc([_make(3)]).execute()
    assert result[0].depth == 3


def test_already_sorted_unchanged():
    result = SortQueryBlocksByDepthDesc([_make(2), _make(1), _make(0)]).execute()
    assert [s.depth for s in result] == [2, 1, 0]


def test_all_same_depth():
    result = SortQueryBlocksByDepthDesc([_make(1), _make(1), _make(1)]).execute()
    assert all(s.depth == 1 for s in result)
    assert len(result) == 3


def test_empty_input():
    result = SortQueryBlocksByDepthDesc([]).execute()
    assert result == []
