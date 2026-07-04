from infrastructure.duckdb.run_subqueries import run_subqueries
from api.schemas.run_query import SubqueryAnalyzeResultList


class SubqueryRunner:
    def __init__(self, subqueries: SubqueryAnalyzeResultList):
        self.subqueries = subqueries

    def execute(self) -> SubqueryAnalyzeResultList:
        self.subqueries = run_subqueries(self.subqueries)
        return self.subqueries
