from dataclasses import dataclass


# クエリ全体・CTE・サブクエリの1ブロック分の内部表現（構造情報のみ）
# テーブル参照の抽出・解決はtable_reference.analyze_table_referencesが担う
@dataclass
class QueryBlock:
    start_index: int
    end_index: int
    query: str
    depth: int
    parent_alias: str | None = None
