from dataclasses import dataclass

import sqlglot
from api.services.query_structure.depth_analyzer import get_query_block_depths
from api.services.query_structure.query_parser import parse_query_block
from api.services.query_structure.range_finder import (
    find_cte_ranges,
    find_subquery_ranges,
)
from api.services.query_structure.table_name_extractor import (
    extract_table_names_with_alias,
)


@dataclass
class QueryBlock:
    start_index: int
    end_index: int
    query: str
    depth: int
    tables_name_alias: list[tuple[str | None, str | None]]
    parent_alias: str | None = None


class QueryStructureBuilder:
    def __init__(self, query: str):
        self.query = query
        self._tokens = sqlglot.tokens.Tokenizer().tokenize(query)

    def execute(self) -> list[QueryBlock]:
        return self._build()

    def _build(self) -> list[QueryBlock]:
        subquery_ranges_alias = find_subquery_ranges(self.query, self._tokens)
        cte_ranges_alias = find_cte_ranges(self._tokens)
        ranges = list(subquery_ranges_alias.keys())
        depths = get_query_block_depths(ranges)
        queries = [self.query[start:end] for start, end in ranges]
        # expressions は、queries を sqlglot でパースした AST（exp.Expression）のリスト
        # 例: "SELECT id FROM users"
        # -> Select(expressions=[Column(...)], from_=From(this=Table(...)))
        expressions = [parse_query_block(query) for query in queries]
        query_block_tables_name_alias = [
            extract_table_names_with_alias(expression) for expression in expressions
        ]

        query_blocks = []
        for (start, end), query, depth, tables_name_alias in zip(
            ranges, queries, depths, query_block_tables_name_alias
        ):
            query_blocks.append(
                QueryBlock(
                    start_index=start,
                    end_index=end,
                    query=query,
                    depth=depth,
                    tables_name_alias=tables_name_alias,
                    parent_alias=cte_ranges_alias.get((start, end))
                    or subquery_ranges_alias.get((start, end)),
                )
            )

        return query_blocks
