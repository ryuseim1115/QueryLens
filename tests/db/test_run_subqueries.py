import pytest

from api.db.run_subqueries import run_subqueries
from api.schemas.run_query import SubqueryAnalyzeResult


def _make(query: str) -> SubqueryAnalyzeResult:
    return SubqueryAnalyzeResult(
        start_index=0,
        end_index=len(query),
        query=query,
        depth=0,
        result=[],
    )


def test_simple_select_returns_rows():
    result = run_subqueries([_make("SELECT id, name FROM users WHERE id = 1")])
    assert len(result[0].result) == 1
    assert result[0].result[0]["name"] == "山田太郎"


def test_aggregate_returns_count():
    result = run_subqueries([_make("SELECT COUNT(*) AS cnt FROM users")])
    assert result[0].result[0]["cnt"] == 20


def test_filter_returns_subset():
    result = run_subqueries([_make("SELECT COUNT(*) AS cnt FROM products WHERE category = '食品'")])
    assert result[0].result[0]["cnt"] == 5


def test_multiple_subqueries_execute_independently():
    subqueries = [
        _make("SELECT COUNT(*) AS cnt FROM users"),
        _make("SELECT COUNT(*) AS cnt FROM products"),
    ]
    result = run_subqueries(subqueries)
    assert result[0].result[0]["cnt"] == 20
    assert result[1].result[0]["cnt"] == 20


def test_join_query_returns_results():
    query = (
        "SELECT u.name, o.amount "
        "FROM users AS u JOIN orders AS o ON u.id = o.user_id "
        "ORDER BY o.id LIMIT 1"
    )
    result = run_subqueries([_make(query)])
    assert len(result[0].result) == 1
    assert result[0].result[0]["name"] == "山田太郎"


def test_invalid_query_raises():
    with pytest.raises(ValueError, match="サブクエリの実行に失敗しました"):
        run_subqueries([_make("SELECT * FROM nonexistent_xyz")])
