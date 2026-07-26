import pytest
import sqlglot
from api.services.query_structure.query_parser import parse_query_block


def test_parse_query_block_raises_on_invalid_query():
    with pytest.raises(sqlglot.errors.ParseError):
        parse_query_block("SELECT FROM WHERE")


def test_offset_is_zero_for_plain_query():
    _, offset = parse_query_block("SELECT * FROM users")
    assert offset == 0


def test_offset_accounts_for_leading_whitespace():
    _, offset = parse_query_block("  SELECT * FROM users")
    assert offset == 2


def test_offset_accounts_for_stripped_parens():
    # "(SELECT * FROM users)" のうち、剥がされる"("の分だけoffsetが増える
    _, offset = parse_query_block("(SELECT * FROM users)")
    assert offset == 1
