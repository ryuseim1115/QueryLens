from fastapi import APIRouter, Depends, HTTPException

from api.dependencies.require_login import require_login
from api.schemas.run_query import QueryInfo, RunQueryResponse
from api.services.analyze_subquery.query_structure_analyzer import (
    QueryStructureAnalyzer,
)
from api.services.analyze_subquery.sort_subquery import SortSubqueryByDepthDesc
from api.services.analyze_subquery.subquery_runner import SubqueryRunner
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
        subqueries = QueryStructureAnalyzer(body.query).execute()
        subqueries = SortSubqueryByDepthDesc(subqueries).execute()
        subqueries = SubqueryRunner(subqueries).execute()
        return RunQueryResponse(subqueries=subqueries)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
