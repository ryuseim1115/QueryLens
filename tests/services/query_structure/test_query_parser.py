import pytest
import sqlglot
from api.services.query_structure.query_parser import parse_query_block


def test_parse_query_block_raises_on_invalid_query():
    with pytest.raises(sqlglot.errors.ParseError):
        parse_query_block("SELECT FROM WHERE")
