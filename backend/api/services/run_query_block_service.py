from typing import Any

from api.validators.query_validator import QueryValidator
from infrastructure.duckdb.run_query import run_query


def run_query_block(user_id: int, database_type: str, query: str) -> list[dict[str, Any]]:
    QueryValidator(database_type, query, user_id).validate()
    return run_query(user_id, query)
