import sqlglot
from sqlglot import exp


# queryをパースしてASTを返すと同時に、剥がした空白/括弧の分だけ
# 元のquery内での文字位置とのズレを表すoffsetを返す
# （ASTノードのmeta["start"]/["end"]はパース対象文字列内での相対位置のため、
#  元のquery文字列上の絶対位置に戻すにはこのoffsetを加算する必要がある）
def parse_query_block(query: str) -> tuple[exp.Expression, int]:
    stripped = query.strip()
    offset = len(query) - len(query.lstrip())

    # サブクエリブロック単体が渡された場合、外側の括弧があると
    # sqlglot がパースできないため剥がす（例: "(SELECT ...)" → "SELECT ..."）
    if stripped.startswith("(") and stripped.endswith(")"):
        inner = stripped[1:-1]
        inner_stripped = inner.strip()
        offset += 1 + (len(inner) - len(inner.lstrip()))
        stripped = inner_stripped

    return sqlglot.parse_one(stripped), offset
