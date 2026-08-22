# QueryLens

複雑なSQLを分解し、中間テーブルをプレビュー表示する解析ツール。

複数のテーブルが絡み合うSQLは、若手エンジニアにとって理解が難しく、指導員が口頭で解説する工数もかさみがちです。QueryLensはSQLを分割し、各フェーズの中間テーブルを可視化することで、指導員と若手が同じ画面を見ながら認識をすり合わせられるようにします。

▶ [アプリを使う](https://querylensapp.com/)

## 主な機能

- **中間テーブル可視化**: 解析結果に基づくテーブルリレーションの表示
- **中間結果プレビュー**: 任意の結合フェーズ・サブクエリを選択し、その時点の抽出結果をプレビュー表示（1リクエストあたり先頭1,000件まで）

## 技術スタック

**バックエンド**

- Python 3.14 / FastAPI / uvicorn
- [sqlglot](https://github.com/tobymao/sqlglot): SQLパース
- [DuckDB](https://duckdb.org/): アップロードされたファイルに対するクエリ実行
- MySQL（SQLAlchemy + PyMySQL）: ユーザー情報の永続化
- Poetry: 依存管理
- [ruff](https://github.com/astral-sh/ruff): lint / format

**フロントエンド**

- Vanilla JavaScript / HTML / CSS（フレームワーク非依存）
- ESLint / Prettier / Stylelint / HTMLHint

## ディレクトリ構成

```
backend/
  api/            ルーター・スキーマ・サービス・バリデータ
  infrastructure/ DuckDB・MySQL・ディスク・セキュリティ等の実装詳細
  main.py         FastAPIエントリポイント
frontend/
  html/           画面テンプレート
  js/              画面ロジック（pages/ 配下がページ、api/ がAPIクライアント）
  css/
data/
  csv_files/      ユーザーごとのアップロード済みCSV
  duckdb/         ユーザーごとのDuckDBファイル
docs/             要件・設計ドキュメント
tests/            pytest
```

## 開発者向け

ローカルで動かす・コントリビュートする場合の情報です。

### セットアップ

**必要なもの**

- Python 3.14+
- Poetry 2.0+
- MySQL（ユーザー登録・ログイン機能に使用）
- Node.js 20+（フロントエンドのlint/formatを行う場合のみ）

**インストール**

```bash
git clone https://github.com/ryuseim1115/QueryLens.git
cd QueryLens
poetry install
```

**環境変数**

プロジェクトルートに `.env` を作成し、以下を設定します。

```
MYSQL_URL=mysql+pymysql://<user>:<password>@<host>/<database>
```

`DATA_DIR` / `DUCKDB_DIR` / `CSV_DISK_DIR` は未指定の場合、リポジトリ直下の `data/` 配下が使われます（`backend/config.py` 参照）。

### 起動

```bash
source <(poetry env activate)
cd backend
uvicorn main:app --reload
```

### テスト・Lint

```bash
# バックエンドのテスト
poetry run pytest

# バックエンドのlint / format
poetry run ruff check .
poetry run ruff format --check .

# フロントエンドのlint / format（frontend/ 配下で実行）
cd frontend
npm install
npm run lint
npx prettier --check "**/*.{js,html,css}"
```

### ブランチ運用

- `develop`: 開発用ブランチ
- `production`: 本番ブランチ。`production` へのPRは `develop` からのみ許可（CIで強制）
- `production` へのpushで EC2 へ自動デプロイ
