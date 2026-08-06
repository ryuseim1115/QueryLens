from dataclasses import dataclass


# クエリ全体・CTE・サブクエリの1ブロック分の内部表現
# （API応答用スキーマへの変換・参照解決はresolve_table_referencesが担う）
@dataclass
class QueryBlock:
    start_index: int
    end_index: int
    query: str
    depth: int
    tables_name_alias: list[tuple[str | None, str | None, tuple[int, int] | None]]
    parent_alias: str | None = None
