from fastapi import APIRouter, Depends

from api.dependencies.require_login import require_login_api
from api.schemas.run_query import RunQueryBlockRequest, RunQueryBlockResponse
from api.services import run_query_block_service

router = APIRouter()


@router.post(
    "/run-query-block",
    response_model=RunQueryBlockResponse,
)
def run_query_block(
    body: RunQueryBlockRequest, user_id: int = Depends(require_login_api)
):
    records = run_query_block_service.run_query_block(
        user_id, body.database_type, body.query
    )
    return RunQueryBlockResponse(records=records)
