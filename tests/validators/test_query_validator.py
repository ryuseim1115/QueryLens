import pytest
from api.validators.query_validator import QueryValidator

TEST_USER_ID = 1


def test_valid_select_passes():
    validator = QueryValidator("duckdb", "SELECT * FROM users", TEST_USER_ID)
    expression = validator.validate()
    assert expression.key == "select"


def test_select_with_where_passes():
    validator = QueryValidator(
        "duckdb", "SELECT id, name FROM users WHERE age > 30", TEST_USER_ID
    )
    expression = validator.validate()
    assert expression.key == "select"


def test_join_query_passes():
    query = (
        "SELECT u.name, o.amount FROM users AS u JOIN orders AS o ON u.id = o.user_id"
    )
    validator = QueryValidator("duckdb", query, TEST_USER_ID)
    expression = validator.validate()
    assert expression.key == "select"


def test_subquery_in_where_passes():
    query = (
        "SELECT * FROM orders WHERE user_id IN (SELECT id FROM users WHERE age > 30)"
    )
    validator = QueryValidator("duckdb", query, TEST_USER_ID)
    expression = validator.validate()
    assert expression.key == "select"


def test_cte_query_passes():
    query = (
        "WITH top_users AS (SELECT id FROM users WHERE age > 30) "
        "SELECT * FROM top_users"
    )
    validator = QueryValidator("duckdb", query, TEST_USER_ID)
    expression = validator.validate()
    assert expression.key == "select"


def test_non_select_raises():
    validator = QueryValidator(
        "duckdb", "INSERT INTO users VALUES (21, 'test', 'x@x.com', 25)", TEST_USER_ID
    )
    with pytest.raises(ValueError, match="SELECT文以外"):
        validator.validate()


def test_invalid_syntax_raises():
    validator = QueryValidator("duckdb", "(", TEST_USER_ID)
    with pytest.raises(ValueError, match="SQL構文"):
        validator.validate()


def test_missing_table_raises():
    validator = QueryValidator(
        "duckdb", "SELECT * FROM nonexistent_table", TEST_USER_ID
    )
    with pytest.raises(ValueError, match="ファイルがアップロードされていません"):
        validator.validate()


def test_multiple_missing_tables_raises():
    validator = QueryValidator(
        "duckdb", "SELECT * FROM foo JOIN bar ON foo.id = bar.id", TEST_USER_ID
    )
    with pytest.raises(ValueError, match="ファイルがアップロードされていません"):
        validator.validate()


def test_other_users_table_is_not_visible():
    validator = QueryValidator("duckdb", "SELECT * FROM users", user_id=999)
    with pytest.raises(ValueError, match="ファイルがアップロードされていません"):
        validator.validate()
