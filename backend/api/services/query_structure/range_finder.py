import sqlglot


def find_subquery_ranges(query: str, tokens: list) -> dict[tuple[int, int], str | None]:
    if not tokens:
        return {}
    subquery_ranges: dict[tuple[int, int], str | None] = {}
    stack = []
    T = sqlglot.tokens.TokenType
    for i, token in enumerate(tokens):
        if token.token_type == T.L_PAREN:
            next_token = tokens[i + 1] if i + 1 < len(tokens) else None
            if next_token and next_token.token_type == T.SELECT:
                stack.append(token.start)
            else:
                stack.append(False)
        elif token.token_type == T.R_PAREN:
            if stack:
                start = stack.pop()
                if start is not False:
                    next_token = tokens[i + 1] if i + 1 < len(tokens) else None
                    if next_token is None:
                        alias = None
                    elif next_token.token_type == T.ALIAS:
                        alias_token = tokens[i + 2] if i + 2 < len(tokens) else None
                        alias = alias_token.text if alias_token else None
                    elif next_token.token_type == T.VAR:
                        alias = next_token.text
                    else:
                        alias = None
                    subquery_ranges[(start, token.end + 1)] = alias

    subquery_ranges[(tokens[0].start, tokens[-1].end + 1)] = None
    return dict(sorted(subquery_ranges.items()))


def find_cte_ranges(tokens: list) -> dict[tuple[int, int], str]:
    T = sqlglot.tokens.TokenType
    cte_ranges: dict[tuple[int, int], str] = {}
    for i, token in enumerate(tokens):
        if token.token_type != T.L_PAREN:
            continue
        next_token = tokens[i + 1] if i + 1 < len(tokens) else None
        if not (next_token and next_token.token_type == T.SELECT):
            continue
        if i < 2:
            continue
        prev1 = tokens[i - 1]
        prev2 = tokens[i - 2]
        if prev1.text.upper() != "AS":
            continue
        cte_name = prev2.text
        depth = 1
        for k in range(i + 1, len(tokens)):
            if tokens[k].token_type == T.L_PAREN:
                depth += 1
            elif tokens[k].token_type == T.R_PAREN:
                depth -= 1
                if depth == 0:
                    cte_ranges[(token.start, tokens[k].end + 1)] = cte_name
                    break
    return cte_ranges
