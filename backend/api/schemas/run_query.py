from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class QueryInfo(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )
    database_type: str
    query: str


class TableInfo(BaseModel):
    table_name: str | None = None
    alias: str | None = None
    # このテーブル名/エイリアスが元クエリ文字列上に実際に書かれている位置
    # （テーブル名のみをハイライトする用途）
    start_index: int | None = None
    end_index: int | None = None
    # 実テーブルではなく別のクエリブロック（CTE/サブクエリ）を指している場合の、
    # 参照先ブロック自体の位置
    referenced_block_start_index: int | None = None
    referenced_block_end_index: int | None = None


class QueryBlockAnalyzeResult(BaseModel):
    start_index: int
    end_index: int
    query: str
    depth: int
    tables_name_alias: list[TableInfo] = []
    parent_alias: str | None = None
    result: list[dict[str, Any]]


QueryBlockAnalyzeResultList = list[QueryBlockAnalyzeResult]


class AnalyzeQueryResponse(BaseModel):
    query_blocks: list[QueryBlockAnalyzeResult]


class RunQueryBlockRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )
    database_type: str
    query: str


class RunQueryBlockResponse(BaseModel):
    records: list[dict[str, Any]]
    truncated: bool
