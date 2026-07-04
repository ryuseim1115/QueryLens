from api.schemas.run_query import SubqueryAnalyzeResultList
from infrastructure.duckdb.run_subqueries import run_subqueries


class SubqueryRunner:
    def __init__(self, subqueries: SubqueryAnalyzeResultList):
        self.subqueries = subqueries

    def execute(self) -> SubqueryAnalyzeResultList:
        self.subqueries = run_subqueries(self.subqueries)
        return self.subqueries
