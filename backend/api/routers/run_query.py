from fastapi import APIRouter, Depends, HTTPException

from api.dependencies.require_login import require_login
from api.schemas.run_query import QueryInfo, RunQueryResponse
from api.services.query_structure.query_structure_analyzer import (
    QueryStructureAnalyzer,
)
from api.services.query_structure.query_block_runner import QueryBlockRunner
from api.services.query_structure.sort_query_blocks import SortQueryBlocksByDepthDesc
from api.validators.query_validator import QueryValidator

router = APIRouter()


@router.post(
    "/run-query",
    response_model=RunQueryResponse,
    dependencies=[Depends(require_login)],
)
def run_query(body: QueryInfo):
    try:
        QueryValidator(body.database_type, body.query).validate()
        query_blocks = QueryStructureAnalyzer(body.query).execute()
        query_blocks = SortQueryBlocksByDepthDesc(query_blocks).execute()
        query_blocks = QueryBlockRunner(query_blocks).execute()
        return RunQueryResponse(query_blocks=query_blocks)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
