from fastapi import APIRouter, Depends, HTTPException

from api.dependencies.require_login import require_login_api
from api.schemas.run_query import QueryInfo, RunQueryResponse
from api.services.query_structure.query_block_runner import QueryBlockRunner
from api.services.query_structure.query_structure_analyzer import (
    QueryStructureAnalyzer,
)
from api.services.query_structure.sort_query_blocks import SortQueryBlocksByDepthDesc
from api.validators.query_validator import QueryValidator

router = APIRouter()


@router.post(
    "/run-query",
    response_model=RunQueryResponse,
)
def run_query(body: QueryInfo, user_id: int = Depends(require_login_api)):
    try:
        QueryValidator(body.database_type, body.query, user_id).validate()
        query_blocks = QueryStructureAnalyzer(body.query).execute()
        query_blocks = SortQueryBlocksByDepthDesc(query_blocks).execute()
        query_blocks = QueryBlockRunner(user_id, query_blocks).execute()
        return RunQueryResponse(query_blocks=query_blocks)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
