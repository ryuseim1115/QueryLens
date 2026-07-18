# QueryLens 詳細設計書 — Post-Analyzer

| 項目 | 内容 |
| --- | --- |
| ドキュメント名 | QueryLens_Detailed_Design_Post_Analyzer |
| 対象ブランチ | refactor-subquery-analysis / feat-display-query-result |
| 作成日 | 2026-05-02 |
| 概要 | SQLクエリを受け取り、クエリブロック（サブクエリ/CTE）単位に分解・実行し結果を表示するPost-Analyzerコンポーネントの詳細設計。 |

## 処理フロー — 具体例によるクエリ分解の流れ

以下の入力クエリを例に、`POST /run-query` で受け取ってから結果を返すまでに各コンポーネントがクエリをどう加工するかを示す（値は実際にバックエンドのコードを実行して得たもの）。

### 入力クエリ

```sql
SELECT o.id, s.total
FROM orders o
JOIN (
    SELECT customer_id, SUM(amount) AS total
    FROM payments
    WHERE amount > 0
    GROUP BY customer_id
) s ON o.customer_id = s.customer_id
```

### 1. QueryValidator.validate()

sqlglotでパースしSELECT文であることを確認。`orders`・`payments`という実テーブル名（CTE名は除く）がDuckDBの`SHOW TABLES`結果に存在するかを検証する。

### 2. QueryStructureBuilder._build() — クエリブロックへの分解

`find_subquery_ranges()`が丸括弧の対応関係をトークン列から追跡し、`(`の直後が`SELECT`であるものだけをサブクエリ範囲として検出する。今回は括弧が1組（`JOIN (...)`）あるため、「クエリ全体」と「その内側のサブクエリ」の2つの範囲が見つかる。`find_cte_ranges()`はWITH句がないため空。`get_query_block_depths()`は各範囲について「自分を完全に包含する範囲の数」を数えることで深さを求める。

| # | start_index | end_index | depth | parent_alias | tables_name_alias | query（先頭） |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 187 | 0 | null | `orders`(alias: o), (name: null, alias: s) | `SELECT o.id, s.total FROM orders o JOIN (...` |
| 1 | 40 | 152 | 1 | `s` | `payments`(alias: null) | `(SELECT customer_id, SUM(amount) AS total FROM...` |

- #0（クエリ全体）: `FROM orders o` → `("orders", "o")`、`JOIN (subquery) s` → `(None, "s")`。サブクエリの中身（`payments`）はここでは見ない。
- #1（内側サブクエリ）: 括弧の直後のトークンが `VAR("s")` なので `parent_alias = "s"` として親クエリでの呼び名を記録。中では `FROM payments` のみを見るので `("payments", None)`。

### 3. SortQueryBlocksByDepthDesc.execute()

depth降順に並べ替える。実行順は `#1（depth=1, payments集計）→ #0（depth=0, クエリ全体）` となる。

### 4. QueryBlockRunner / run_query_blocks() — 各ブロックを個別にDuckDBで実行

**重要な点**: 内側の結果を外側に差し込んで組み立て直すわけではない。各ブロックの `query` テキスト（切り出した元のSQLそのもの）を、そのままDuckDBに対して独立に実行し、それぞれの結果を格納する。これにより「クエリのどの部分が、どのデータを返しているか」をブロック単位で可視化できる。

- ブロック#1 `(SELECT customer_id, SUM(amount) AS total FROM payments WHERE amount > 0 GROUP BY customer_id)` を実行
  → 例: `[{"customer_id": 1, "total": 3200}, {"customer_id": 2, "total": 900}]`
- ブロック#0 `SELECT o.id, s.total FROM orders o JOIN (...) s ON o.customer_id = s.customer_id` を実行（サブクエリを含んだ元のクエリそのものなのでDuckDB自身がJOINを解決する）
  → 例: `[{"id": 101, "total": 3200}, {"id": 102, "total": 900}]`

### 5. APIレスポンス（RunQueryResponse）

```json
{
  "query_blocks": [
    {
      "start_index": 0,
      "end_index": 187,
      "query": "SELECT o.id, s.total\nFROM orders o\nJOIN (\n ... \n) s ON o.customer_id = s.customer_id",
      "depth": 0,
      "tables_name_alias": [
        { "name": "orders", "alias": "o" },
        { "name": null, "alias": "s" }
      ],
      "parent_alias": null,
      "result": [
        { "id": 101, "total": 3200 },
        { "id": 102, "total": 900 }
      ]
    },
    {
      "start_index": 40,
      "end_index": 152,
      "query": "(\n    SELECT customer_id, SUM(amount) AS total\n    FROM payments\n ... \n)",
      "depth": 1,
      "tables_name_alias": [
        { "name": "payments", "alias": null }
      ],
      "parent_alias": "s",
      "result": [
        { "customer_id": 1, "total": 3200 },
        { "customer_id": 2, "total": 900 }
      ]
    }
  ]
}
```

### 6. フロントエンドでの表示

- `displayQuery()`: 入力クエリ全文をそのまま表示。
- `displayTables()`: `depth`ごとにグループ化してテーブルカード（`orders`, `payments`）を描画。クリックで`start_index`〜`end_index`の範囲を`highlightQuery()`でハイライト。
- `displayLines()`: 各ブロックの`parent_alias`（例: ブロック#1の`"s"`）を親グループ内から`findParentAliasEl()`で探し、canvas上に依存線を描画。
- `displayQueryResult()`: テーブルカードクリック時に、そのブロックの`result`（例: ブロック#1なら`customer_id`/`total`の2行）を表として再描画。
