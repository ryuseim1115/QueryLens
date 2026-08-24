from typing import Any, Self

from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.alias_generators import to_camel

from api.validators.query_validator import parse_select_query


class QueryInfo(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )
    database_type: str
    query: str

    # SELECT文以外を拒否する。テーブル存在チェック（QueryValidator._validate_tables）は
    # user_idというリクエストボディ外の情報に依存するためサービス層に残しているが、
    # この構文チェックはdatabase_type/queryだけで完結するため、
    # ここで型ヒント駆動に強制する
    @model_validator(mode="after")
    def _validate_query(self) -> Self:
        parse_select_query(self.database_type, self.query)
        return self


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
    table_references: list[TableInfo] = []
    parent_alias: str | None = None


QueryBlockAnalyzeResultList = list[QueryBlockAnalyzeResult]


class AnalyzeQueryResponse(BaseModel):
    query_blocks: list[QueryBlockAnalyzeResult]


class RunQueryBlockRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )
    database_type: str
    query: str

    @model_validator(mode="after")
    def _validate_query(self) -> Self:
        parse_select_query(self.database_type, self.query)
        return self


class RunQueryBlockResponse(BaseModel):
    records: list[dict[str, Any]]
    truncated: bool
