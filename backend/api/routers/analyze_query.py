from fastapi import APIRouter, Depends

from api.dependencies.require_login import require_login_api
from api.schemas.run_query import AnalyzeQueryResponse, QueryInfo
from api.services import analyze_query_service

router = APIRouter()


@router.post(
    "/analyze-query",
    response_model=AnalyzeQueryResponse,
)
def analyze_query(body: QueryInfo, user_id: int = Depends(require_login_api)):
    query_blocks = analyze_query_service.analyze_query(
        user_id, body.database_type, body.query
    )
    return AnalyzeQueryResponse(query_blocks=query_blocks)
