import sqlglot
from sqlglot import exp


def parse_query_block(query: str) -> exp.Expression:
    query = query.strip()
    # サブクエリブロック単体が渡された場合、外側の括弧があると
    # sqlglot がパースできないため剥がす（例: "(SELECT ...)" → "SELECT ..."）
    if query.startswith("(") and query.endswith(")"):
        query = query[1:-1].strip()
    return sqlglot.parse_one(query)
