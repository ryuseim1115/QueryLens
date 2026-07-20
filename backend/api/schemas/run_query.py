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
    name: str | None = None
    alias: str | None = None


class QueryBlockAnalyzeResult(BaseModel):
    start_index: int
    end_index: int
    query: str
    depth: int
    tables_name_alias: list[TableInfo] = []
    parent_alias: str | None = None
    result: list[dict[str, Any]]


QueryBlockAnalyzeResultList = list[QueryBlockAnalyzeResult]


class RunQueryResponse(BaseModel):
    query_blocks: list[QueryBlockAnalyzeResult]


class RunQueryBlockRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )
    database_type: str
    query: str
    start_index: int


class RunQueryBlockResponse(BaseModel):
    query_block: QueryBlockAnalyzeResult
