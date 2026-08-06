import sqlglot

T = sqlglot.tokens.TokenType


# ブロック（クエリ全体・CTE・サブクエリ）ごとの(start, end)範囲と、
# CTE名 or サブクエリの末尾エイリアスを1回のトークン走査でまとめて特定する
def find_block_ranges_with_alias(query: str) -> dict[tuple[int, int], str | None]:
    tokens = sqlglot.tokens.Tokenizer().tokenize(query)
    if not tokens:
        return {}
    ranges_alias: dict[tuple[int, int], str | None] = {}
    # 開き括弧ごとに(開始位置, CTE名 or None)を積む。SELECTで始まらない括弧
    # （関数呼び出し等）はFalseを積んで対応関係だけ保つ
    stack: list[tuple[int, str | None] | bool] = []

    for i, token in enumerate(tokens):
        if token.token_type == T.L_PAREN:
            next_token = tokens[i + 1] if i + 1 < len(tokens) else None
            if next_token and next_token.token_type == T.SELECT:
                stack.append((token.start, _find_cte_name(tokens, i)))
            else:
                stack.append(False)
        elif token.token_type == T.R_PAREN and stack:
            open_paren = stack.pop()
            if open_paren is False:
                continue
            start, cte_name = open_paren
            alias = cte_name or _find_subquery_alias(tokens, i)
            ranges_alias[(start, token.end + 1)] = alias

    # クエリ全体自身も1ブロックとして扱う（エイリアスは存在しないためNone）
    ranges_alias[(tokens[0].start, tokens[-1].end + 1)] = None
    return dict(sorted(ranges_alias.items()))


# 開き括弧の直前が「識別子 AS」ならCTE定義とみなし、名前を返す
# 例: "WITH t AS (SELECT ...)" の "(" では tokens[i-2]="t", tokens[i-1]="AS"
def _find_cte_name(tokens: list, l_paren_index: int) -> str | None:
    i = l_paren_index
    if i >= 2 and tokens[i - 1].token_type == T.ALIAS:
        return tokens[i - 2].text
    return None


# CTEでない場合、閉じ括弧の直後を見てサブクエリのエイリアスを返す
def _find_subquery_alias(tokens: list, r_paren_index: int) -> str | None:
    i = r_paren_index
    next_token = tokens[i + 1] if i + 1 < len(tokens) else None
    # 例: "(SELECT * FROM b) AS c"　cを取得する
    if next_token and next_token.token_type == T.ALIAS:
        alias_token = tokens[i + 2] if i + 2 < len(tokens) else None
        return alias_token.text if alias_token else None
    # 例: "(SELECT * FROM b) c" 　cを取得する
    if next_token and next_token.token_type == T.VAR:
        return next_token.text
    return None
